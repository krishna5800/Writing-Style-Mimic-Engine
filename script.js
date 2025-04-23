document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const generateButton = document.getElementById('generateButton');
    const compareButton = document.getElementById('compareButton');
    const promptInput = document.getElementById('promptInput');
    const styleSelect = document.getElementById('styleSelect');
    const customStyleContainer = document.getElementById('customStyleContainer');
    const customStyle = document.getElementById('customStyle');
    const generatedText = document.getElementById('generatedText');
    const generationStatus = document.getElementById('generationStatus');
    const copyOutput = document.getElementById('copyOutput');
    const downloadOutput = document.getElementById('downloadOutput');
    const text1 = document.getElementById('text1');
    const text2 = document.getElementById('text2');
    const comparisonResult = document.getElementById('comparisonResult');
    const scoreValue = document.getElementById('scoreValue');
    const scoreBar = document.getElementById('scoreBar');
    const similarityDescription = document.getElementById('similarityDescription');
    const verdictValue = document.getElementById('verdictValue');
    const verdictConfidence = document.getElementById('verdictConfidence');
    const verdictExplanation = document.getElementById('verdictExplanation');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingMessage = document.getElementById('loadingMessage');
    const scrollToGenerate = document.getElementById('scrollToGenerate');
    const scrollToCompare = document.getElementById('scrollToCompare');
    const useImprovedModel = document.getElementById('useImprovedModel');
    
    // Event Listeners
    styleSelect.addEventListener('change', toggleCustomStyle);
    generateButton.addEventListener('click', generateText);
    compareButton.addEventListener('click', compareTexts);
    copyOutput.addEventListener('click', copyToClipboard);
    downloadOutput.addEventListener('click', downloadText);
    scrollToGenerate.addEventListener('click', () => scrollToSection('generate'));
    scrollToCompare.addEventListener('click', () => scrollToSection('compare'));
    
    // Functions
    function toggleCustomStyle() {
      if (styleSelect.value === 'custom') {
        customStyleContainer.classList.remove('hidden');
      } else {
        customStyleContainer.classList.add('hidden');
      }
    }
    
    function scrollToSection(sectionId) {
      document.getElementById(sectionId).scrollIntoView({ behavior: 'smooth' });
    }
    
    async function generateText() {
      const prompt = promptInput.value.trim();
      const style = styleSelect.value === 'custom' ? customStyle.value.trim() : styleSelect.value;
      
      if (!prompt) {
        showStatus('Please enter a prompt', 'error');
        return;
      }
      
      if (styleSelect.value === 'custom' && !style) {
        showStatus('Please describe the custom style', 'error');
        return;
      }
      
      showLoading('Generating text...');
      
      try {
        // Simulate API call (replace with actual API call)
        const response = await simulateApiCall({
          prompt,
          style,
          action: 'generate'
        });
        
        generatedText.textContent = response.generatedText;
        showStatus('Text generated successfully', 'success');
      } catch (error) {
        console.error('Error generating text:', error);
        showStatus('Failed to generate text', 'error');
      } finally {
        hideLoading();
      }
    }
    
    async function compareTexts() {
      const text1Value = text1.value.trim();
      const text2Value = text2.value.trim();
      const improvedModel = useImprovedModel.checked;
      
      if (!text1Value || !text2Value) {
        showStatus('Please enter both texts to compare', 'error');
        return;
      }
      
      showLoading('Comparing texts...');
      comparisonResult.classList.add('hidden');
      
      try {
        // Simulate API call (replace with actual API call)
        const response = await simulateApiCall({
          text1: text1Value,
          text2: text2Value,
          improvedModel,
          action: 'compare'
        });
        
        // Update UI with comparison results
        scoreValue.textContent = `${response.similarityScore}%`;
        scoreBar.style.width = `${response.similarityScore}%`;
        similarityDescription.textContent = response.similarityDescription;
        
        verdictValue.textContent = response.sameAuthor ? 'Likely' : 'Unlikely';
        verdictValue.style.backgroundColor = response.sameAuthor ? 'var(--success-color)' : 'var(--error-color)';
        verdictValue.style.color = 'white';
        
        verdictConfidence.textContent = `Confidence: ${response.confidence}%`;
        verdictExplanation.textContent = response.verdictExplanation;
        
        comparisonResult.classList.remove('hidden');
        showStatus('Comparison completed', 'success');
      } catch (error) {
        console.error('Error comparing texts:', error);
        showStatus('Failed to compare texts', 'error');
      } finally {
        hideLoading();
      }
    }
    
    function copyToClipboard() {
      const text = generatedText.textContent;
      if (!text || text === 'Your generated text will appear here...') {
        showStatus('Nothing to copy', 'warning');
        return;
      }
      
      navigator.clipboard.writeText(text)
        .then(() => showStatus('Copied to clipboard', 'success'))
        .catch(err => {
          console.error('Failed to copy:', err);
          showStatus('Failed to copy', 'error');
        });
    }
    
    function downloadText() {
      const text = generatedText.textContent;
      if (!text || text === 'Your generated text will appear here...') {
        showStatus('Nothing to download', 'warning');
        return;
      }
      
      const blob = new Blob([text], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'generated-text.txt';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      showStatus('Download started', 'success');
    }
    
    function showStatus(message, type) {
      generationStatus.textContent = message;
      generationStatus.style.backgroundColor = 
        type === 'success' ? 'var(--success-color)' :
        type === 'error' ? 'var(--error-color)' :
        type === 'warning' ? 'var(--warning-color)' : 'transparent';
      generationStatus.style.color = type ? 'white' : 'inherit';
      
      setTimeout(() => {
        generationStatus.textContent = 'Ready';
        generationStatus.style.backgroundColor = 'transparent';
        generationStatus.style.color = 'inherit';
      }, 3000);
    }
    
    function showLoading(message) {
      loadingMessage.textContent = message;
      loadingOverlay.classList.remove('hidden');
    }
    
    function hideLoading() {
      loadingOverlay.classList.add('hidden');
    }
    
    // Simulate API call (replace with actual fetch to your backend)
    function simulateApiCall(data) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          if (Math.random() < 0.05) { // 5% chance of failure for simulation
            reject(new Error('Simulated API failure'));
            return;
          }
          
          if (data.action === 'generate') {
            resolve({
              generatedText: generateSimulatedText(data.prompt, data.style)
            });
          } else if (data.action === 'compare') {
            const similarityScore = Math.floor(Math.random() * 100);
            const sameAuthor = similarityScore > 70;
            
            resolve({
              similarityScore,
              sameAuthor,
              confidence: Math.floor(Math.random() * 30) + 70,
              similarityDescription: getRandomDescription(similarityScore),
              verdictExplanation: sameAuthor ? 
                'The texts share significant stylistic similarities that suggest they may have been written by the same author.' :
                'The texts show notable differences in style, making it unlikely they were written by the same author.'
            });
          }
        }, 1500);
      });
    }
    
    function generateSimulatedText(prompt, style) {
      const styles = {
        formal: `Upon careful consideration of the prompt "${prompt}", it becomes evident that a formal approach would be most appropriate. The subject matter warrants thorough examination and systematic analysis to ensure comprehensive understanding.`,
        casual: `So, I was thinking about "${prompt}" and honestly, it's pretty interesting stuff! Like, who would've thought, right? Anyway, here's what I came up with - it's not perfect but it's something.`,
        technical: `The input "${prompt}" can be analyzed through the following technical framework. Parameters include lexical density (0.72), syntactic complexity (1.8), and semantic coherence (92%). Preliminary results indicate a strong correlation with established patterns in this domain.`,
        creative: `The whisper of "${prompt}" danced through the autumn leaves, a secret carried on the wind. It twirled and spun, painting the sky with stories untold, until at last it settled in my heart, transformed into this:`,
        shakespearean: `"${prompt}", quoth he, and verily did the assembled masses ponder this most curious utterance. Forsooth, what meaning could lie therein? Hark, and I shall weave for thee a tale most wondrous, spun from this very thread.`,
        hemingway: `It was a clean, well-lighted place. The man thought about "${prompt}". He drank his whiskey. The whiskey was good. It burned going down. He thought some more. This is what he thought.`,
        academic: `The phenomenon described as "${prompt}" has been extensively studied in recent literature (Smith et al., 2020; Johnson, 2018). Current research suggests a multifactorial etiology, with significant implications for future theoretical frameworks.`,
        journalistic: `BREAKING: New developments in "${prompt}" have shocked experts. Sources close to the matter reveal startling details that could change everything we know. Our investigative team has uncovered the following exclusive information.`,
        custom: `[In the style of ${style}] The prompt "${prompt}" evokes a particular sensibility. It calls to mind the nuanced approach characteristic of this style, blending distinctive elements to create a cohesive whole that resonates with readers.`
      };
      
      return styles[style] || styles.formal;
    }
    
    function getRandomDescription(score) {
      const descriptions = [
        `The texts share ${score}% similarity in writing style. This includes comparable sentence structure, word choice, and thematic elements.`,
        `With a ${score}% similarity score, these texts demonstrate ${score > 50 ? 'significant' : 'moderate'} overlap in stylistic features like tone and narrative voice.`,
        `Analysis reveals ${score}% stylistic similarity, particularly in ${score > 70 ? 'multiple key areas' : 'certain aspects'} of linguistic patterning and rhetorical devices.`,
        `The ${score}% similarity score indicates ${score > 60 ? 'a strong' : 'some'} correlation between the texts' use of figurative language and syntactic patterns.`
      ];
      
      return descriptions[Math.floor(Math.random() * descriptions.length)];
    }
  });