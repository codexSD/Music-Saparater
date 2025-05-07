document.addEventListener('DOMContentLoaded', function() {
  // DOM Elements
  const form = document.getElementById('uploadForm');
  const fileInput = document.getElementById('fileInput');
  const processBtn = document.getElementById('processBtn');
  const optionCards = document.querySelectorAll('.option-card');
  const isolationType = document.getElementById('isolationType');
  const fileDropArea = document.getElementById('fileDropArea');
  const fileInfo = document.getElementById('fileInfo');
  const fileName = document.getElementById('fileName');
  const fileSize = document.getElementById('fileSize');
  const removeFile = document.getElementById('removeFile');
  const progressArea = document.getElementById('progressArea');
  const progressBar = document.getElementById('progressBar');
  const statusText = document.getElementById('statusText');
  const downloadArea = document.getElementById('downloadArea');
  const downloadLink = document.getElementById('downloadLink');
  const settingsToggle = document.getElementById('settingsToggle');
  const settingsContent = document.getElementById('settingsContent');
  const advancedSettingsForm = document.getElementById('advancedSettingsForm');
  const qualitySlider = document.getElementById('qualitySlider');
  const qualityValue = document.getElementById('qualityValue');
  const noiseReductionCheck = document.getElementById('noiseReductionCheck');
  const stemBalanceSlider = document.getElementById('stemBalanceSlider');
  const stemBalanceValue = document.getElementById('stemBalanceValue');
  
  // Input file handling
  if (fileInput) {
    fileInput.addEventListener('change', handleFileSelect);
  }

  // Drag and drop handling
  if (fileDropArea) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      fileDropArea.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
      fileDropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      fileDropArea.addEventListener(eventName, unhighlight, false);
    });

    fileDropArea.addEventListener('drop', handleDrop, false);
    fileDropArea.addEventListener('click', () => fileInput.click());
  }

  // Remove file button
  if (removeFile) {
    removeFile.addEventListener('click', resetFileInput);
  }

  // Option cards selection
  if (optionCards.length > 0) {
    optionCards.forEach(card => {
      card.addEventListener('click', () => {
        optionCards.forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        if (isolationType) {
          isolationType.value = card.getAttribute('data-value');
        }
      });
    });
  }

  // Settings toggle
  if (settingsToggle && settingsContent) {
    settingsToggle.addEventListener('click', () => {
      settingsToggle.classList.toggle('open');
      settingsContent.classList.toggle('visible');
    });
  }

  // Quality slider
  if (qualitySlider && qualityValue) {
    qualitySlider.addEventListener('input', () => {
      qualityValue.textContent = `${qualitySlider.value}%`;
    });
  }

  // Stem balance slider
  if (stemBalanceSlider && stemBalanceValue) {
    stemBalanceSlider.addEventListener('input', () => {
      const value = parseInt(stemBalanceSlider.value);
      if (value === 0) {
        stemBalanceValue.textContent = 'Balanced';
      } else if (value < 0) {
        stemBalanceValue.textContent = `${Math.abs(value)}% more vocals`;
      } else {
        stemBalanceValue.textContent = `${value}% more music`;
      }
    });
  }

  // Form submission
  if (form) {
    form.addEventListener('submit', handleFormSubmit);
  }

  // Functions
  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  function highlight() {
    fileDropArea.classList.add('dragover');
  }

  function unhighlight() {
    fileDropArea.classList.remove('dragover');
  }

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length) {
      fileInput.files = files;
      handleFileSelect();
    }
  }

  function handleFileSelect() {
    if (fileInput.files.length) {
      const file = fileInput.files[0];
      const validExtensions = ['.mp3', '.wav', '.mp4', '.mkv', '.mov'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
      
      if (!validExtensions.includes(fileExtension)) {
        alert('Please select a valid audio or video file (MP3, WAV, MP4, MKV, MOV)');
        resetFileInput();
        return;
      }

      updateFileInfo(file);
      fileDropArea.classList.add('has-file');
      processBtn.disabled = false;
    } else {
      resetFileInput();
    }
  }

  function updateFileInfo(file) {
    fileInfo.classList.add('visible');
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
  }

  function resetFileInput() {
    fileInput.value = '';
    fileInfo.classList.remove('visible');
    fileDropArea.classList.remove('has-file');
    processBtn.disabled = true;
  }

  function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  function handleFormSubmit(e) {
    e.preventDefault();
    
    // Show progress
    progressArea.classList.add('visible');
    downloadArea.classList.remove('visible');
    processBtn.disabled = true;
    
    // Create FormData
    const formData = new FormData(form);
    
    // Add advanced settings if they exist
    if (advancedSettingsForm) {
      const qualityValue = qualitySlider ? qualitySlider.value : 100;
      formData.append('quality', qualityValue);
      
      if (noiseReductionCheck && noiseReductionCheck.checked) {
        formData.append('noise_reduction', 'true');
      }
      
      if (stemBalanceSlider) {
        formData.append('stem_balance', stemBalanceSlider.value);
      }
    }
    
    // Update progress display
    let progress = 0;
    const progressInterval = setInterval(() => {
      progress += (100 - progress) / 30;
      if (progress > 95) progress = 95;
      updateProgress(progress);
    }, 500);
    
    // Send request
    fetch('/process', {
      method: 'POST',
      body: formData
    })
    .then(response => {
      clearInterval(progressInterval);
      
      if (!response.ok) {
        return response.json().then(err => { throw new Error(err.detail || 'Error processing file'); });
      }
      
      // Get filename
      const contentDisposition = response.headers.get('Content-Disposition');
      let outputFileName = fileInput.files[0].name;
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
        if (filenameMatch && filenameMatch[1]) {
          outputFileName = filenameMatch[1];
        }
      }
      
      // Complete progress
      updateProgress(100);
      
      // Convert to blob and create download link
      return response.blob().then(blob => {
        const url = URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.download = outputFileName;
        
        // Show download section
        progressArea.classList.remove('visible');
        downloadArea.classList.add('visible');
        
        // Add to processing history if available
        if (typeof addToHistory === 'function') {
          const isolationTypeText = document.querySelector('.option-card.selected h3').textContent;
          addToHistory(outputFileName, isolationTypeText, url);
        }
      });
    })
    .catch(error => {
      clearInterval(progressInterval);
      console.error('Error:', error);
      statusText.textContent = `Error: ${error.message}`;
      statusText.classList.add('error');
      processBtn.disabled = false;
    });
  }

  function updateProgress(value) {
    progressBar.style.width = `${value}%`;
    const label = value < 100 ? `Processing... ${Math.round(value)}%` : 'Processing complete!';
    statusText.textContent = label;
  }

  // Processing history feature
  const historyList = document.getElementById('historyList');
  const historyTab = document.getElementById('historyTab');
  
  // Initialize processing history from localStorage
  if (historyList && historyTab) {
    historyTab.addEventListener('click', () => {
      const historyItems = getHistoryItems();
      renderHistoryItems(historyItems);
    });
  }
  
  function addToHistory(fileName, type, blobUrl) {
    const historyItems = getHistoryItems();
    const timestamp = new Date().toISOString();
    
    historyItems.unshift({
      id: Date.now(),
      fileName,
      type,
      timestamp,
      blobUrl
    });
    
    // Keep only the last 10 items
    if (historyItems.length > 10) {
      historyItems.pop();
    }
    
    localStorage.setItem('processingHistory', JSON.stringify(historyItems));
    
    // If we're on the history tab, refresh the display
    if (historyList && historyList.closest('.tab-content').classList.contains('active')) {
      renderHistoryItems(historyItems);
    }
  }
  
  function getHistoryItems() {
    const historyData = localStorage.getItem('processingHistory');
    return historyData ? JSON.parse(historyData) : [];
  }
  
  function renderHistoryItems(items) {
    if (!historyList) return;
    
    if (items.length === 0) {
      historyList.innerHTML = '<div class="no-history">No processing history yet</div>';
      return;
    }
    
    historyList.innerHTML = '';
    
    items.forEach(item => {
      const date = new Date(item.timestamp);
      const formattedDate = date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
      
      const historyItem = document.createElement('div');
      historyItem.className = 'history-item';
      historyItem.innerHTML = `
        <div class="history-item-details">
          <div class="history-item-name">${item.fileName}</div>
          <div class="history-item-meta">
            <span class="history-item-type">${item.type}</span>
            <span class="history-item-date">${formattedDate}</span>
          </div>
        </div>
        <div class="history-item-actions">
          <a href="${item.blobUrl}" download="${item.fileName}" class="btn btn-sm">Download</a>
        </div>
      `;
      
      historyList.appendChild(historyItem);
    });
  }

  // Tabs functionality
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');
  
  if (tabButtons.length && tabContents.length) {
    tabButtons.forEach(button => {
      button.addEventListener('click', () => {
        // Deactivate all tabs
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));
        
        // Activate clicked tab
        button.classList.add('active');
        const targetId = button.getAttribute('data-target');
        document.getElementById(targetId).classList.add('active');
        
        // Load history if needed
        if (targetId === 'historyTab' && typeof getHistoryItems === 'function') {
          renderHistoryItems(getHistoryItems());
        }
      });
    });
  }
  
  // Audio preview functionality (for batch processing)
  const previewButtons = document.querySelectorAll('.preview-audio');
  
  if (previewButtons.length) {
    previewButtons.forEach(button => {
      button.addEventListener('click', function() {
        const audioUrl = this.getAttribute('data-audio');
        const audioPlayer = document.getElementById('audioPreviewPlayer');
        
        if (audioPlayer) {
          audioPlayer.src = audioUrl;
          audioPlayer.play();
        }
      });
    });
  }
}); 