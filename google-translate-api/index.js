const express = require('express');
const translate = require('google-translate-extended-api');
const app = express();

app.use(express.json());


dataOptions = {
    returnRawResponse: false,
    detailedTranslations: true,
    definitionSynonyms: true,
    detailedTranslationsSynonyms: true,
    definitions: true,
    definitionExamples: true,
    examples: true,
    removeStyles: true
}

app.post('/translate', (req, res) => {
    const {text, source_lang, dest_lang} = req.body;
    translate(text, source_lang, dest_lang, dataOptions)
        .then(response => res.json(response))
        .catch(error => res.status(500).json({error: error.message}));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
