/* ===============================
   GLOBAL STATE
================================ */
let moviesData = [];
let wishlist = JSON.parse(localStorage.getItem("wishlist")) || [];
let currentSlide = 0;

/* ===============================
   THEME TOGGLE
================================ */
/* ===============================
   THEME TOGGLE
================================ */
function toggleTheme() {
    const body = document.body;
    const btn = document.querySelector(".theme-toggle");

    body.classList.toggle("light-theme");

    if (body.classList.contains("light-theme")) {
        btn.textContent = "☀️";
        localStorage.setItem("theme", "light");
    } else {
        btn.textContent = "🌙";
        localStorage.setItem("theme", "dark");
    }
}

// Load saved theme
(function () {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "light") {
        document.body.classList.add("light-theme");
        document.querySelector(".theme-toggle").textContent = "☀️";
    }
})();


/* ===============================
   LOAD MOVIES FROM DJANGO API
================================ */
async function loadMovies() {
    try {
        const res = await fetch("/movies/api/movies/");

        // 🔴 Agar API error de
        if (!res.ok) {
            throw new Error("API not reachable");
        }

        const data = await res.json();

        // 🔴 Safety check
        if (!data.movies) {
            console.error("Invalid API response", data);
            return;
        }

        moviesData = data.movies;
        renderMovies(moviesData);

    } catch (error) {
        console.error("API Error:", error);
    }
}


/* ===============================
   RENDER MOVIES
================================ */
function renderMovies(list) {
    const grid = document.getElementById("moviesGrid");
    grid.innerHTML = "";

    list.forEach(movie => {
        const inWishlist = wishlist.find(w => w.id === movie.id);

        grid.innerHTML += `
        <div class="movie-card">
            <button class="add-to-wishlist ${inWishlist ? "in-wishlist" : ""}"
                onclick="toggleWishlist(${movie.id})">❤️</button>

            <img src="${movie.image}"
            alt="${movie.title}"
            class="movie-poster"
                 onerror="this.onerror=null;this.src='https://picsum.photos/400/600';">

        


            <div class="movie-info">
                <h3>${movie.title}</h3>
                <p class="genre">${movie.genres.join(" / ")}</p>
                <p class="rating">⭐ ${movie.rating}</p>
            </div>
        </div>`;
    });

    updateWishlistCount();
}

/* ===============================
   SEARCH
================================ */
function searchMovies() {
    const q = document.getElementById("searchInput").value.toLowerCase();
    const filtered = moviesData.filter(m => m.title.toLowerCase().includes(q));
    renderMovies(filtered);
}

/* ===============================
   WISHLIST
================================ */
function toggleWishlist(id) {
    const movie = moviesData.find(m => m.id === id);
    const index = wishlist.findIndex(m => m.id === id);

    if (index === -1) wishlist.push(movie);
    else wishlist.splice(index, 1);

    localStorage.setItem("wishlist", JSON.stringify(wishlist));
    renderMovies(moviesData);
}

function updateWishlistCount() {
    document.getElementById("wishlistCount").innerText = wishlist.length;
}

function openWishlist() {
    document.getElementById("wishlistModal").style.display = "block";
}

function closeWishlist() {
    document.getElementById("wishlistModal").style.display = "none";
}

/* ===============================
   LOGIN
================================ 
function openLogin() {
    document.getElementById("loginModal").style.display = "block";
}

function closeLogin() {
    document.getElementById("loginModal").style.display = "none";
}
*/


/* ===============================
   RECOMMENDATIONS
================================ */
async function getRecommendations() {
    const movie = prompt("Enter movie title:");
    if (!movie) return;

    const res = await fetch(`/movies/content/?title=${movie}`);
    const data = await res.json();

    alert("Recommended: " + data.recommendations.join(", "));
}

/* ===============================
   INIT
================================ */
loadMovies();
updateWishlistCount();


document.addEventListener("DOMContentLoaded", () => {
    loadMovies();
});


console.log("Movies from API:", data.movies);
console.log(moviesData);
