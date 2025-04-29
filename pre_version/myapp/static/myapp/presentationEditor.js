console.log("==== Updated presentationEditor.js ====");

let slides = [];
let currentSlide = 0;
let isSaving = false; // 这个是用来存储保存状态的

// DOM Elements
const prevButton = document.getElementById("prevSlide");
const nextButton = document.getElementById("nextSlide");
const slideIndicator = document.getElementById("slideIndicator");
const slideThumbnail = document.getElementById("slideThumbnail");
const scriptTextarea = document.getElementById("scriptTextarea");
const thumbnailList = document.getElementById("thumbnailList");
const charCount = document.getElementById("charCount");
const generateVideoButton = document.getElementById("generateVideoButton");

// 从URL获取process_id
const urlParams = new URLSearchParams(window.location.search);
const processId = urlParams.get('process_id');

generateVideoButton.addEventListener('click', async function (e) {
    e.preventDefault();

    const loadingDiv = document.getElementById('loading');
    try {
        loadingDiv.style.display = 'flex';
        const response = await fetch('/generate_video/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: new URLSearchParams({ process_id: processId })
        });

        const data = await response.json();
        if (response.ok) {
            const videoContainer = document.createElement('div');
            videoContainer.style.marginTop = '20px';
            videoContainer.innerHTML = `
                <p>Video generated successfully!</p>
                <a href="${data.video_url}" 
                   download 
                   class="button"
                   style="display: inline-block; margin-top: 10px;">
                   Download Video
                </a>
                <video controls style="width: 100%; margin-top: 10px;">
                    <source src="${data.video_url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            `;
            document.querySelector('main').after(videoContainer);
        } else {
            alert('Error: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error generating video:', error);
        alert('Network error: ' + error.message);
    } finally {
        loadingDiv.style.display = 'none';
    }
});

// 初始化演示文稿
async function initializePresentation() {
    showLoading(true);

    try {
        // 1. 获取基本数据
        const dataRes = await fetch(`/get_slides_data/?process_id=${processId}`);
        if (!dataRes.ok) throw new Error('Failed to load slides data');
        const data = await dataRes.json();

        // 2. 初始化slides数组
        slides = Array.from({ length: data.num_pages }, (_, index) => ({
            id: index + 1,
            thumbnail: `${data.image_base_url}page_${index + 1}.png`,
            textEndpoint: `${data.text_api_endpoint}&page=${index + 1}`,
            script: 'Loading...'
        }));

        // 3. 加载所有文本内容
        await Promise.all(slides.map(async (slide, index) => {
            const textRes = await fetch(slide.textEndpoint);
            if (!textRes.ok) throw new Error('Failed to load text');
            const { text } = await textRes.json();
            slides[index].script = text;
        }));

        // 4. 初始化界面
        updateSlide();
    } catch (error) {
        console.error('Initilization failed:', error);
        alert(`Loading failed: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// 显示加载动画
function showLoading(show) {
    const loadingDiv = document.getElementById('loading');
    if (loadingDiv) loadingDiv.style.display = show ? 'flex' : 'none';
}

// 更新幻灯片界面
function updateSlide() {
    const slide = slides[currentSlide];

    // 更新缩略图
    slideThumbnail.src = slide.thumbnail;
    slideThumbnail.onerror = () => {
        slideThumbnail.src = 'https://via.placeholder.com/800x600?text=图片加载失败';
    };

    // 更新其他UI元素
    slideIndicator.textContent = `Slide ${currentSlide + 1} / ${slides.length}`;
    scriptTextarea.value = slide.script;
    charCount.textContent = `${slide.script.length} Chars`;

    // 按钮状态
    prevButton.disabled = currentSlide === 0;
    nextButton.disabled = currentSlide === slides.length - 1;

    // 更新缩略图列表
    thumbnailList.innerHTML = '';

    let start, end;

    if (currentSlide === 0) {
        // 第一张幻灯片：显示第1、2、3张
        start = 0;
        end = Math.min(3, slides.length);
    } else if (currentSlide === slides.length - 1) {
        // 最后一张幻灯片：显示倒数第3、2、1张
        start = Math.max(0, slides.length - 3);
        end = slides.length;
    } else {
        // 中间幻灯片：显示当前幻灯片及其前后各一张
        start = currentSlide - 1;
        end = currentSlide + 2;
    }

    for (let i = start; i < end; i++) {
        const slideItem = slides[i];
        const button = document.createElement("button");
        button.className = `thumbnail-item${i === currentSlide ? ' selected' : ''}`;
        button.innerHTML = `
            <img src="${slideItem.thumbnail}" 
                 alt="Page ${i + 1}" 
                 class="thumbnail"
                 onerror="this.src='https://via.placeholder.com/150x100?text=缩略图错误'">
        `;
        button.onclick = () => changeSlide(i);
        thumbnailList.appendChild(button);
    }
}

// 切换幻灯片并保存当前内容
async function changeSlide(newIndex) {
    if (isSaving) return; // 防止重复保存

    // 显示保存状态
    const savingDiv = document.getElementById('savingStatus');
    savingDiv.style.display = 'block';
    isSaving = true;

    try {
        // 保存当前幻灯片内容
        const currentPage = currentSlide + 1;
        const response = await fetch('/save_script/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: new URLSearchParams({
                process_id: processId,
                page: currentPage,
                content: slides[currentSlide].script
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Save Error');
        }

        // 切换幻灯片
        currentSlide = newIndex;
        updateSlide();
    } catch (error) {
        console.error('Save Error:', error);
        alert(`Automatic Save Error: ${error.message}`);
    } finally {
        savingDiv.style.display = 'none';
        isSaving = false;
    }
}

// 获取 CSRF Token
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return decodeURIComponent(value);
    }
    return null;
}

// 事件监听
prevButton.addEventListener("click", async () => {
    if (currentSlide > 0) await changeSlide(currentSlide - 1);
});

nextButton.addEventListener("click", async () => {
    if (currentSlide < slides.length - 1) await changeSlide(currentSlide + 1);
});

scriptTextarea.addEventListener("input", (e) => {
    slides[currentSlide].script = e.target.value;
    charCount.textContent = `${e.target.value.length} 字符`;
});

// 启动初始化
initializePresentation();
