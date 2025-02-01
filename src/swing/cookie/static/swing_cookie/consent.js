document.getElementById('cookie-consent-form').onsubmit = function(event) {
    event.preventDefault();
    var consent = event.submitter.value;
    fetch("{% url 'cookie_consent' %}", {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
        },
        body: new URLSearchParams({
            'consent': consent
        })
    }).then(response => {
        if (response.ok) {
            alert('Your preference has been saved.');
        }
    });
};