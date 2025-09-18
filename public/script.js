document.getElementById('analysis-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const form = event.target;
    const fileInput = document.getElementById('file');
    const queryInput = document.getElementById('query');
    const resultsContainer = document.getElementById('results-container');
    const loadingSpinner = document.getElementById('loading-spinner');

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('query', queryInput.value || 'Analyze this financial document for investment insights');

    resultsContainer.classList.add('hidden');
    loadingSpinner.classList.remove('hidden');

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'An error occurred');
        }

        const data = await response.json();
        
        const converter = new showdown.Converter({ tables: true });
        
        document.querySelector('#financial-analysis .markdown-content').innerHTML = converter.makeHtml(data.analysis.financial_analysis);
        document.querySelector('#investment-advice .markdown-content').innerHTML = converter.makeHtml(data.analysis.investment_advice);
        document.querySelector('#risk-assessment .markdown-content').innerHTML = converter.makeHtml(data.analysis.risk_assessment);

        resultsContainer.classList.remove('hidden');
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        loadingSpinner.classList.add('hidden');
    }
});
