/**
 * Swing Cookie Consent JavaScript Module
 * =======================================
 *
 * Provides cookie consent management with event hooks for integration
 * with analytics, marketing tools, and other cookie-dependent features.
 *
 * Events:
 * -------
 * - cookieConsentUpdated: Fired when consent status changes
 * - cookieConsentRequired: Fired when user needs to provide consent
 * - cookieConsentLoaded: Fired when consent status is loaded from server
 *
 * Usage:
 * ------
 * document.addEventListener('cookieConsentUpdated', (e) => {
 *   if (e.detail.groups.analytics?.accepted) {
 *     // Initialize analytics
 *   }
 * });
 */

(function(window, document) {
  'use strict';

  const SwingCookieConsent = {
    config: {
      statusUrl: '/cookie-consent/status/',
      preferencesUrl: '/cookie-consent/preferences/',
      acceptUrl: '/cookie-consent/accept/',
      declineUrl: '/cookie-consent/decline/',
      withdrawUrl: '/cookie-consent/withdraw/',
    },

    state: {
      loaded: false,
      consentGiven: false,
      groups: {},
      csrfToken: null,
    },

    /**
     * Initialize the consent module
     * @param {Object} options - Configuration options
     */
    init: function(options) {
      if (options) {
        Object.assign(this.config, options);
      }

      // Load current consent status
      this.loadStatus().then(() => {
        this.state.loaded = true;
        this._dispatchEvent('cookieConsentLoaded', this.state);

        // Check if consent is needed
        if (!this.state.consentGiven && this._hasPendingGroups()) {
          this._dispatchEvent('cookieConsentRequired', {
            groups: this.state.groups,
          });
        }
      });

      // Set up form handlers
      this._setupFormHandlers();
    },

    /**
     * Load consent status from server
     * @returns {Promise}
     */
    loadStatus: function() {
      return fetch(this.config.statusUrl, {
        method: 'GET',
        headers: {
          'X-Cookie-Consent-Fetch': '1',
        },
      })
      .then(response => response.json())
      .then(data => {
        this.state.consentGiven = data.consent_given;
        this.state.groups = data.groups;
        this.state.csrfToken = data.csrf_token;
        return data;
      })
      .catch(error => {
        console.error('Failed to load consent status:', error);
        throw error;
      });
    },

    /**
     * Accept a specific cookie group or all groups
     * @param {string|null} varname - Group varname, or null for all
     * @returns {Promise}
     */
    accept: function(varname) {
      const url = varname
        ? `${this.config.acceptUrl}${varname}/`
        : this.config.acceptUrl;

      return this._submitConsent(url, varname, true);
    },

    /**
     * Decline a specific cookie group or all groups
     * @param {string|null} varname - Group varname, or null for all
     * @returns {Promise}
     */
    decline: function(varname) {
      const url = varname
        ? `${this.config.declineUrl}${varname}/`
        : this.config.declineUrl;

      return this._submitConsent(url, varname, false);
    },

    /**
     * Withdraw all consent
     * @returns {Promise}
     */
    withdrawAll: function() {
      return fetch(this.config.withdrawUrl, {
        method: 'POST',
        headers: this._getHeaders(),
      })
      .then(response => {
        if (response.ok) {
          // Reset state
          Object.keys(this.state.groups).forEach(key => {
            this.state.groups[key].accepted = false;
            this.state.groups[key].declined = true;
            this.state.groups[key].pending = false;
          });
          this.state.consentGiven = false;

          this._dispatchEvent('cookieConsentUpdated', {
            action: 'withdraw_all',
            groups: this.state.groups,
          });
        }
        return response;
      });
    },

    /**
     * Update preferences for multiple groups at once
     * @param {Object} preferences - Object mapping varname to boolean
     * @returns {Promise}
     */
    updatePreferences: function(preferences) {
      return fetch(this.config.preferencesUrl, {
        method: 'POST',
        headers: {
          ...this._getHeaders(),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(preferences),
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Update local state
          Object.keys(preferences).forEach(varname => {
            if (this.state.groups[varname]) {
              const accepted = preferences[varname];
              this.state.groups[varname].accepted = accepted;
              this.state.groups[varname].declined = !accepted;
              this.state.groups[varname].pending = false;
            }
          });

          this.state.consentGiven = Object.values(this.state.groups)
            .some(g => g.accepted);

          this._dispatchEvent('cookieConsentUpdated', {
            action: 'update_preferences',
            updated: data.updated,
            groups: this.state.groups,
          });
        }
        return data;
      });
    },

    /**
     * Check if a specific cookie group is accepted
     * @param {string} varname - Group varname
     * @returns {boolean}
     */
    isAccepted: function(varname) {
      return this.state.groups[varname]?.accepted || false;
    },

    /**
     * Check if a specific cookie group is required
     * @param {string} varname - Group varname
     * @returns {boolean}
     */
    isRequired: function(varname) {
      return this.state.groups[varname]?.is_required || false;
    },

    /**
     * Get all accepted group varnames
     * @returns {string[]}
     */
    getAcceptedGroups: function() {
      return Object.entries(this.state.groups)
        .filter(([_, group]) => group.accepted)
        .map(([varname, _]) => varname);
    },

    // =========================================================================
    // Private Methods
    // =========================================================================

    _submitConsent: function(url, varname, accepted) {
      return fetch(url, {
        method: 'POST',
        headers: this._getHeaders(),
      })
      .then(response => {
        if (response.ok) {
          // Update local state
          if (varname && this.state.groups[varname]) {
            this.state.groups[varname].accepted = accepted;
            this.state.groups[varname].declined = !accepted;
            this.state.groups[varname].pending = false;
          } else if (!varname) {
            // All groups
            Object.keys(this.state.groups).forEach(key => {
              if (!this.state.groups[key].is_required || accepted) {
                this.state.groups[key].accepted = accepted;
                this.state.groups[key].declined = !accepted;
                this.state.groups[key].pending = false;
              }
            });
          }

          this.state.consentGiven = Object.values(this.state.groups)
            .some(g => g.accepted);

          this._dispatchEvent('cookieConsentUpdated', {
            action: accepted ? 'accept' : 'decline',
            varname: varname,
            groups: this.state.groups,
          });

          // Execute deferred scripts if accepting
          if (accepted) {
            this._executeDeferredScripts(varname);
          }
        }
        return response;
      });
    },

    _getHeaders: function() {
      const headers = {
        'X-Cookie-Consent-Fetch': '1',
      };
      if (this.state.csrfToken) {
        headers['X-CSRFToken'] = this.state.csrfToken;
      }
      return headers;
    },

    _hasPendingGroups: function() {
      return Object.values(this.state.groups).some(g => g.pending);
    },

    _dispatchEvent: function(eventName, detail) {
      const event = new CustomEvent(eventName, {
        bubbles: true,
        detail: detail,
      });
      document.dispatchEvent(event);
    },

    _executeDeferredScripts: function(varname) {
      const scripts = document.querySelectorAll("script[type='x/cookie_consent']");
      scripts.forEach(script => {
        const scriptVarname = script.getAttribute('data-varname');
        if (!varname || scriptVarname === varname) {
          if (this.isAccepted(scriptVarname)) {
            const src = script.getAttribute('src');
            if (src) {
              const newScript = document.createElement('script');
              newScript.src = src;
              document.head.appendChild(newScript);
            } else {
              eval(script.innerHTML);
            }
            script.remove();
          }
        }
      });
    },

    _setupFormHandlers: function() {
      // Handle consent forms
      document.addEventListener('submit', (e) => {
        const form = e.target.closest('[data-cookie-consent-form]');
        if (!form) return;

        e.preventDefault();

        const action = e.submitter?.value || form.dataset.action || 'accept';
        const varname = form.dataset.varname || null;

        if (action === 'accept') {
          this.accept(varname);
        } else if (action === 'decline') {
          this.decline(varname);
        } else if (action === 'withdraw') {
          this.withdrawAll();
        } else if (action === 'preferences') {
          // Collect checkbox values
          const preferences = {};
          form.querySelectorAll('input[type="checkbox"][data-varname]').forEach(input => {
            preferences[input.dataset.varname] = input.checked;
          });
          this.updatePreferences(preferences);
        }
      });

      // Handle simple consent buttons
      document.addEventListener('click', (e) => {
        const button = e.target.closest('[data-cookie-consent]');
        if (!button) return;

        e.preventDefault();

        const action = button.dataset.cookieConsent;
        const varname = button.dataset.varname || null;

        if (action === 'accept') {
          this.accept(varname);
        } else if (action === 'decline') {
          this.decline(varname);
        } else if (action === 'withdraw') {
          this.withdrawAll();
        }
      });
    },
  };

  // Export to window
  window.SwingCookieConsent = SwingCookieConsent;

  // Auto-initialize if data attribute is present
  if (document.querySelector('[data-cookie-consent-auto-init]')) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => SwingCookieConsent.init());
    } else {
      SwingCookieConsent.init();
    }
  }

})(window, document);
