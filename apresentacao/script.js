document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    let currentSlide = 0;

    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const slideCounter = document.getElementById('slideCounter');
    const progressBar = document.getElementById('progressBar');
    const slideSelect = document.getElementById('slideSelect');
    const toggleNotesBtn = document.getElementById('toggleNotesBtn');
    const notesPanel = document.getElementById('notesPanel');
    const notesContent = document.getElementById('notesContent');
    const fullScreenBtn = document.getElementById('fullScreenBtn');
    const printBtn = document.getElementById('printBtn');

    // Populate Slide Select Dropdown
    slides.forEach((slide, index) => {
        const option = document.createElement('option');
        option.value = index;
        const title = slide.querySelector('.slide-title')?.innerText || (index === 0 ? "Slide Título" : `Slide ${index + 1}`);
        option.text = `${index + 1}. ${title}`;
        slideSelect.appendChild(option);
    });

    function showSlide(index) {
        if (index < 0) index = 0;
        if (index >= totalSlides) index = totalSlides - 1;

        slides[currentSlide].classList.remove('active');
        currentSlide = index;
        slides[currentSlide].classList.add('active');

        // Update UI
        slideCounter.innerText = `Slide ${currentSlide + 1} / ${totalSlides}`;
        progressBar.style.width = `${((currentSlide + 1) / totalSlides) * 100}%`;
        slideSelect.value = currentSlide;

        // Speaker Notes Cues
        const noteText = slides[currentSlide].getAttribute('data-notes') || "Foque na explicação dos tópicos do slide mantendo ritmo entre 10 e 15 minutos.";
        notesContent.innerText = noteText;

        // Button States
        prevBtn.disabled = (currentSlide === 0);
        nextBtn.disabled = (currentSlide === totalSlides - 1);
        prevBtn.style.opacity = (currentSlide === 0) ? "0.5" : "1";
        nextBtn.style.opacity = (currentSlide === totalSlides - 1) ? "0.5" : "1";
    }

    prevBtn.addEventListener('click', () => showSlide(currentSlide - 1));
    nextBtn.addEventListener('click', () => showSlide(currentSlide + 1));
    slideSelect.addEventListener('change', (e) => showSlide(parseInt(e.target.value)));

    toggleNotesBtn.addEventListener('click', () => {
        notesPanel.classList.toggle('visible');
    });

    fullScreenBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    });

    printBtn.addEventListener('click', () => {
        window.print();
    });

    // Keyboard Navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
            showSlide(currentSlide + 1);
        } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
            showSlide(currentSlide - 1);
        } else if (e.key === 'Home') {
            showSlide(0);
        } else if (e.key === 'End') {
            showSlide(totalSlides - 1);
        } else if (e.key.toLowerCase() === 'n') {
            notesPanel.classList.toggle('visible');
        }
    });

    // Initialize First Slide
    showSlide(0);
});
