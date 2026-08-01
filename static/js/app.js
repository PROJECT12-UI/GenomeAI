/* ==========================================================
   GenomeAI JavaScript
========================================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* ==========================
       PAGE LOADER
    ========================== */

    const loader = document.getElementById("page-loader");

    if (loader) {

        setTimeout(() => {

            loader.style.opacity = "0";

            setTimeout(() => {

                loader.style.display = "none";

            }, 500);

        }, 600);

    }

    /* ==========================
       FLASH MESSAGE AUTO HIDE
    ========================== */

    const flashes = document.querySelectorAll(".flash");

    flashes.forEach((flash) => {

        setTimeout(() => {

            flash.style.opacity = "0";

            flash.style.transform = "translateX(100px)";

            setTimeout(() => {

                flash.remove();

            }, 500);

        }, 4000);

    });

    /* ==========================
       RANGE SLIDER
    ========================== */

    const slider = document.getElementById("simulationRange");
    const value = document.getElementById("rangeValue");

    if (slider && value) {

        value.innerHTML = slider.value;

        slider.addEventListener("input", function () {

            value.innerHTML = this.value;

        });

    }

    /* ==========================
       COUNTER ANIMATION
    ========================== */

    const counters = document.querySelectorAll(".stat-number");

    counters.forEach(counter => {

        const target = parseInt(counter.innerText);

        if (isNaN(target)) return;

        let current = 0;

        const step = Math.ceil(target / 60);

        const timer = setInterval(() => {

            current += step;

            if (current >= target) {

                counter.innerText = target;

                clearInterval(timer);

            }

            else {

                counter.innerText = current;

            }

        }, 20);

    });

});


/* ==========================================================
   FILE NAME PREVIEW
========================================================== */

function showMotherFile(input) {

    if (input.files.length > 0) {

        document.getElementById("motherFileName").innerHTML =

            "Selected: " + input.files[0].name;

    }

}

function showFatherFile(input) {

    if (input.files.length > 0) {

        document.getElementById("fatherFileName").innerHTML =

            "Selected: " + input.files[0].name;

    }

}


/* ==========================================================
   CURSOR GLOW
========================================================== */

const glow = document.querySelector(".cursor-glow");

if (glow) {

    document.addEventListener("mousemove", (e) => {

        glow.style.left = e.clientX + "px";

        glow.style.top = e.clientY + "px";

    });

}


/* ==========================================================
   SMOOTH SCROLL
========================================================== */

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        const target = document.querySelector(

            this.getAttribute("href")

        );

        if (!target) return;

        e.preventDefault();

        target.scrollIntoView({

            behavior: "smooth"

        });

    });

});


/* ==========================================================
   SCROLL ANIMATION
========================================================== */

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.classList.add("show");

        }

    });

});

document.querySelectorAll(

    ".feature-card,.upload-card,.summary-card,.stat-box,.analysis-card"

).forEach(el => {

    observer.observe(el);

});


/* ==========================================================
   BUTTON RIPPLE
========================================================== */

document.querySelectorAll(".btn").forEach(button => {

    button.addEventListener("click", function (e) {

        const ripple = document.createElement("span");

        ripple.className = "ripple";

        ripple.style.left =

            e.offsetX + "px";

        ripple.style.top =

            e.offsetY + "px";

        this.appendChild(ripple);

        setTimeout(() => {

            ripple.remove();

        }, 600);

    });

});


/* ==========================================================
   PRINT REPORT
========================================================== */

function printReport() {

    window.print();

}