console.log("==== Using the COMPLETE script.js ====");

document.addEventListener("DOMContentLoaded", function () {
  // ================= 通用工具函数 =================
  function getCookie(name) {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      const [key, value] = cookie.trim().split("=");
      if (key === name) return decodeURIComponent(value);
    }
    return null;
  }

  function setupFileUpload(uploadArea, fileInput, fileNameHandler) {
    // 点击触发文件选择
    uploadArea.addEventListener("click", () => fileInput.click());

    // 拖拽处理
    uploadArea.addEventListener("dragover", (e) => {
      e.preventDefault();
      uploadArea.style.backgroundColor = "#f0f0f0";
    });

    uploadArea.addEventListener("dragleave", () => {
      uploadArea.style.backgroundColor = "";
    });

    uploadArea.addEventListener("drop", (e) => {
      e.preventDefault();
      uploadArea.style.backgroundColor = "";
      if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        fileNameHandler(e.dataTransfer.files[0].name);
      }
    });

    // 文件变化处理
    fileInput.addEventListener("change", (e) => {
      if (e.target.files.length) {
        fileNameHandler(e.target.files[0].name);
      }
    });
  }

  // ================= 语音克隆功能 =================
  let mediaRecorder;
  let audioChunks = [];
  const cloneVoiceBtn = document.getElementById('cloneVoiceBtn');
  const recordingIndicator = document.querySelector('.recording-indicator');

  // 初始化录音功能
  navigator.mediaDevices.getUserMedia({ audio: true })
    .catch(err => {
      console.error('Error accessing microphone:', err);
      cloneVoiceBtn.disabled = true;
      cloneVoiceBtn.textContent = 'Microphone access denied';
    });

  // 处理录音按钮点击
  cloneVoiceBtn.addEventListener('click', async () => {
    if (!mediaRecorder || mediaRecorder.state === 'inactive') {
      startRecording();
    } else {
      stopRecording();
    }
  });

  function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        
        mediaRecorder.ondataavailable = (e) => {
          audioChunks.push(e.data);
        };

        mediaRecorder.onstop = () => {
          const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
          saveRecording(audioBlob);
          audioChunks = [];
        };

        mediaRecorder.start();
        cloneVoiceBtn.classList.add('recording');
        recordingIndicator.classList.add('active');
        cloneVoiceBtn.innerHTML = `<span class="recording-indicator active"></span>Stop Recording`;
      })
      .catch(err => {
        console.error('Error starting recording:', err);
        alert('Error accessing microphone. Please check permissions.');
      });
  }

  function stopRecording() {
    mediaRecorder.stop();
    cloneVoiceBtn.classList.remove('recording');
    recordingIndicator.classList.remove('active');
    cloneVoiceBtn.innerHTML = `<span class="recording-indicator"></span>Start Recording`;
  }
  
  function saveRecording(blob) {
    // 创建FormData发送到后端
    const formData = new FormData();
    formData.append('voice', blob, 'voice.wav');
    
    fetch('/save_voice/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
    .then(response => response.json())
    .then(data => {
      if(data.success) {
        alert('录音已保存到指定路径');
      } else {
        alert('保存失败: ' + data.error);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('保存失败');
    });
  }

  // ================= 视频生成功能 =================
  const videoForm = document.getElementById("videoGeneratorForm");
  const videoFileInput = document.getElementById("file-upload");
  const videoUploadArea = document.getElementById("file-upload-area");

  setupFileUpload(videoUploadArea, videoFileInput, (fileName) => {
    const fileNameElement = document.createElement("p");
    fileNameElement.textContent = `Selected file: ${fileName}`;
    fileNameElement.style.marginTop = "1rem";
    fileNameElement.style.fontWeight = "bold";

    const existingFileName = videoUploadArea.querySelector("p:last-child");
    if (existingFileName?.textContent.startsWith("Selected file:")) {
      videoUploadArea.removeChild(existingFileName);
    }
    videoUploadArea.appendChild(fileNameElement);
  });

  videoForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const file = videoFileInput.files[0];
    if (!file) {
      alert("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("style", document.querySelector('input[name="scriptLevel"]:checked').value);
    formData.append("token_limit", document.querySelector('input[name="scriptLength"]:checked').value);
    formData.append("voice_type", document.getElementById("voice-type").value);

    try {
      const response = await fetch("/process_presentation/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      });

      const data = await response.json();
      console.log("Video Response:", data);

      if (data.redirect_url) {
        window.location.href = data.redirect_url;
      } else if (data.error) {
        alert("Error: " + data.error);
      } else {
        alert("Unexpected response: " + JSON.stringify(data));
      }
    } catch (error) {
      console.error("Video Request failed:", error);
      alert("Network error: " + error.message);
    }
  });

  // ================= PPT生成功能 =================
  const pptForm = document.getElementById("pptGeneratorForm");
  const pptFileInput = document.getElementById("ppt-file-upload");
  const pptUploadArea = document.getElementById("ppt-file-upload-area");

  setupFileUpload(pptUploadArea, pptFileInput, (fileName) => {
    const fileNameElement = document.createElement("p");
    fileNameElement.textContent = `Selected file: ${fileName}`;
    fileNameElement.style.marginTop = "1rem";
    fileNameElement.style.fontWeight = "bold";

    const existingFileName = pptUploadArea.querySelector("p:last-child");
    if (existingFileName?.textContent.startsWith("Selected file:")) {
      pptUploadArea.removeChild(existingFileName);
    }
    pptUploadArea.appendChild(fileNameElement);
  });

  pptForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData();
    
    const pptFile = pptFileInput.files[0];
    if (pptFile) {
      formData.append("file", pptFile);
    }

    formData.append("query", document.getElementById("requirements").value);
    formData.append("template_id", document.getElementById("theme").value);
    formData.append("language", document.getElementById("ppt-language").value);

    try {
      const response = await fetch("/generate_ppt/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      });

      const data = await response.json();
      console.log("PPT Response:", data);

      if (data.ppt_url) {
        window.open(data.ppt_url, "_blank");
      } else if (data.error) {
        alert("Error: " + data.error);
      } else {
        alert("Unexpected response: " + JSON.stringify(data));
      }
    } catch (error) {
      console.error("PPT Request failed:", error);
      alert("Network error: " + error.message);
    }
  });

  // ================= 选项卡切换功能 =================
  document.querySelectorAll('.tab-item').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      
      const targetTab = this.dataset.tab;
      document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
      });
      document.getElementById(`${targetTab}-tab`).classList.add('active');
    });
  });
});