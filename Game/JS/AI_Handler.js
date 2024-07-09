async function getAIAction(state) {
    const response = await fetch('http://127.0.0.1:5000/get_AI_action', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ state: state })
    });

    if (!response.ok) {
        throw new Error('Network response was not ok, because: ' + response.statusText);
    }
    const data = await response.json();
    return data.action;
}

export { getAIAction };
