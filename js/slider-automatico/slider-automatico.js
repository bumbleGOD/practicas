const slides = document.querySelector('.slider-inner');
const images = Array.from(slides.children);
const totalSlides = images.length;

images.forEach(img => {
    const clone = img.cloneNode(true);
    slides.appendChild(clone);
});

let slideIndex = 0;
const moveSlides = () => {
    slideIndex++;
    slides.style.transition = "transform 0.5s ease-in-out";
    slides.style.transform = `translateX(-${slideIndex * 100}%)`;

    if (slideIndex === totalSlides) {
        setTimeout(() => {
            slides.style.transition = "none"; 
            slideIndex = 0; 
            slides.style.transform = `translateX(0)`;
        }, 500);
    }
};

setInterval(moveSlides, 2000);