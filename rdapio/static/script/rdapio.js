(function(self) {
    self.rdapio = {
        lookup: function(domain, svc_name, onAuto, onDoc, onError) {
            var dispatch = function(rdap) {
                for (var i = 0; i < rdap.links.length; i++) {
                    svc = rdap.links[i];
                    url = new URL(svc.href);
                    rel = new URL(svc.rel);

                    if (rel.hostname != 'rdap.io' ||
                        !rel.pathname.endsWith(svc_name)) {
                        continue;
                    }

                    if (rel.pathname.startsWith('/tpda/')) {
                       return onAuto(url);
                    } else if (rel.pathname.startsWith('/doc/')) {
                       return onDoc(url);
                    }
                }
            }

            return fetch('http://rdap.io/domain/' + domain)
                .then(function ready(req) {
                    return req.json();
                }, function error(err) {
                    onError(err);
                    return {'links': []}
                }).then(dispatch);
        },
    },

    self.rdaplet = {
        form: null,
        form_msg: null,
        form_domain : null,
        form_button : null,
        form_doc : null,
        trigger: null,

        override: true,
        svc_name: 'record',
        svc_args: null,
        steps: {
            // 'step': [message, display doc, display button]
            'initial': ['Enter your domain below:', false, false],
            'checking': ['Checking your domain...', false, false],
            'error': ['Failed to fetch domain info', false, false],
            'auto': ['Automatic configuration available', false, true],
            'doc': ['See documentation below', true, false]
        },

        set_step: function(what, docdata) {
            if (this.form_msg) {
                this.form_msg.innerText = this.steps[what][0];
            }

            this.form_doc.hidden = !this.steps[what][1];
            this.form_doc.innerHTML = docdata;
            this.form_button.hidden = !this.steps[what][2];

            if (!this.form_button.hidden) {
                this.form.onsubmit = null;
            } else {
                this.form.onsubmit = function() { return false };
            }
        },

        refresh: function() {
            this.set_step('initial');
            last = Date.time;
            if (this.trigger) {
                clearTimeout(this.trigger);
            }
            this.trigger = setTimeout(this.check.bind(this), 1000);
        },

        check: function() {
            domain = this.form_domain.value;
            if (domain) {
                this.set_step('checking');
                rdapio.lookup(domain, this.svc_name,
                    this.set_autodoc.bind(this), this.set_doc.bind(this),
                    this.set_error.bind(this)); 
            }
        },

        set_error: function(err) {
            this.set_step('error');
            console.log(err);
        },

        set_autodoc: function(url) {
            this.set_step('auto');
            if (this.override) {
                this.form.action = url;
                this.form.method = 'GET';
            }
        },

        set_doc: function(url) {
            fetch(url).then(function ready(req) {
                    return req.text();
                }, function error(req) {
                    return "Error fetching registrar doc";
                }).then(function update(data) {
                    this.set_step('doc', data);
                }.bind(this));
        },


        // "Exported" functions below
        setup: function(fname) {
            this.form = document.getElementById(fname);
            this.form.innerHTML = '';

            this.form_msg = document.createElement('div');
            this.form_msg.classList.add('rdapio');
            this.form.appendChild(this.form_msg);

            this.form_domain = document.createElement('input');
            this.form_domain.type = "text";
            this.form_domain.name = "domain";
            this.form_domain.classList.add('rdapio');
            this.form_domain.autocomplete = "off";

            this.form_domain.oninput = this.refresh.bind(this);
            this.form.appendChild(this.form_domain);

            this.form_button = document.createElement('button');
            this.form_button.innerText = 'Configure';
            this.form_button.classList.add('rdapio');
            this.form.appendChild(this.form_button);

            this.form_doc = document.createElement('div');
            this.form_doc.classList.add('rdapio');
            this.form_doc.id = 'rdapio-doc';
            this.form.appendChild(this.form_doc);

            this.set_step('initial');

            return this;
        },

        for_service: function(svc) {
            this.svc_name = svc;
            return this;
        },

        add_param: function(name, value) {
            input = document.createElement('input');
            input.type = "text";
            input.hidden = true;
            input.name = name;
            input.value = value;
            this.form.appendChild(input);

            return this;
        },

        say_when: function(step, value) {
            this.steps[step][0] = value;
            // ..bah..
            this.set_step('initial');
            return this;
        }
    }
})(typeof self !== 'undefined' ? self : this);
