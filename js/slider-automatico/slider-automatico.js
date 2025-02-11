let slideIndex = 0;
const slides = document.querySelector('.slider-inner');
const totalSlides = slides.children.length;

function showSlides () {
    slideIndex++;
    if (slideIndex >= totalSlides) {
        slideIndex = 0;
    }

    const offset = slideIndex * -100;
    slides.style.transform = `translateX(${offset}%)`;
}

setInterval (showSlides, 3000);