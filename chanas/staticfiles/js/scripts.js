document.addEventListener("DOMContentLoaded", function () {
    const tableRows = document.querySelectorAll("#prestataireTable tr");
    const filterVille = document.getElementById("filterVille");
    const filterType = document.getElementById("filterType");
    const searchInput = document.getElementById("searchInput");
    const noResults = document.getElementById("noResults");

    // Animation d'apparition des lignes
    tableRows.forEach((row, index) => {
        row.style.opacity = "0";
        setTimeout(() => {
            row.style.transition = "opacity 0.5s ease-in-out";
            row.style.opacity = "1";
        }, index * 100);
    });

    // Ajout d'un effet hover sur les lignes du tableau
    tableRows.forEach(row => {
        row.addEventListener("mouseenter", () => {
            row.style.backgroundColor = "#f8f9fa";
            row.style.transition = "background-color 0.3s ease";
        });

        row.addEventListener("mouseleave", () => {
            row.style.backgroundColor = "";
        });
    });

    // Fonction de filtrage
    function filterTable() {
        let villeValue = filterVille.value.toLowerCase();
        let typeValue = filterType.value.toLowerCase();
        let searchValue = searchInput.value.toLowerCase();
        let visibleRows = 0;

        tableRows.forEach(row => {
            let ville = row.querySelector(".ville").textContent.toLowerCase();
            let type = row.querySelector(".type").textContent.toLowerCase();
            let name = row.querySelector("td:first-child").textContent.toLowerCase(); // Nom du prestataire

            if ((villeValue === "" || ville.includes(villeValue)) &&
                (typeValue === "" || type.includes(typeValue)) &&
                (searchValue === "" || name.includes(searchValue))) {
                
                row.style.display = "";
                row.style.opacity = "0";
                setTimeout(() => {
                    row.style.transition = "opacity 0.5s ease-in-out";
                    row.style.opacity = "1";
                }, 100);
                
                visibleRows++;
            } else {
                row.style.opacity = "0";
                setTimeout(() => {
                    row.style.display = "none";
                }, 300);
            }
        });

        // Animation du message "Aucun prestataire trouvé"
        if (visibleRows === 0) {
            noResults.style.display = "block";
            noResults.style.opacity = "0";
            setTimeout(() => {
                noResults.style.transition = "opacity 0.5s ease-in-out";
                noResults.style.opacity = "1";
            }, 100);
        } else {
            noResults.style.opacity = "0";
            setTimeout(() => {
                noResults.style.display = "none";
            }, 300);
        }
    }

    console.log("Le fichier scripts.js est bien chargé !");
    // Ajout des écouteurs d'événements pour les filtres et la recherche
    filterVille.addEventListener("change", filterTable);
    filterType.addEventListener("change", filterTable);
    searchInput.addEventListener("keyup", filterTable);
});