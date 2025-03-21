document.addEventListener("DOMContentLoaded", function () {
    // Sélection des éléments HTML
    const filterVille = document.getElementById("filterVille");
    const filterType = document.getElementById("filterType");
    const entriesSelect = document.getElementById("entriesSelect");
    const searchInput = document.getElementById("searchInput");
    const tableRows = Array.from(document.querySelectorAll("tbody tr"));
    const noResults = document.getElementById("noResults");

    let rowsPerPage = parseInt(entriesSelect.value, 10);
    let currentPage = 1;

    // Fonction de filtrage
    function filterTable() {
        let villeValue = filterVille.value.toLowerCase();
        let typeValue = filterType.value.toLowerCase();
        let searchValue = searchInput.value.toLowerCase();
        let filteredRows = [];

        tableRows.forEach(row => {
            let ville = row.querySelector(".ville").textContent.toLowerCase();
            let type = row.querySelector(".type").textContent.toLowerCase();
            let name = row.querySelector(".nom").textContent.toLowerCase();

            if ((villeValue === "" || ville.includes(villeValue)) &&
                (typeValue === "" || type.includes(typeValue)) &&
                (searchValue === "" || name.includes(searchValue))) {
                filteredRows.push(row);
            }
        });

        // Afficher ou masquer le message "Aucun prestataire trouvé"
        noResults.style.display = filteredRows.length === 0 ? "block" : "none";

        paginateTable(filteredRows);
    }

    // Fonction pour gérer la pagination
    function paginateTable(filteredRows) {
        let totalRows = filteredRows.length;
        let totalPages = Math.ceil(totalRows / rowsPerPage);
        if (currentPage > totalPages) currentPage = totalPages || 1;

        tableRows.forEach(row => row.style.display = "none"); // Cacher toutes les lignes
        let start = (currentPage - 1) * rowsPerPage;
        let end = start + rowsPerPage;

        filteredRows.slice(start, end).forEach(row => row.style.display = ""); // Afficher les bonnes lignes

        updatePaginationControls(totalPages);
    }

    // Fonction pour mettre à jour la pagination
    function updatePaginationControls(totalPages) {
        let paginationContainer = document.getElementById("pagination");
        paginationContainer.innerHTML = "";

        for (let i = 1; i <= totalPages; i++) {
            let btn = document.createElement("button");
            btn.textContent = i;
            btn.className = `page-btn ${i === currentPage ? "active" : ""}`;
            btn.addEventListener("click", function () {
                currentPage = i;
                filterTable();
            });
            paginationContainer.appendChild(btn);
        }
    }

    // Événements
    filterVille.addEventListener("change", filterTable);
    filterType.addEventListener("change", filterTable);
    searchInput.addEventListener("keyup", filterTable);
    entriesSelect.addEventListener("change", function () {
        rowsPerPage = parseInt(entriesSelect.value, 10);
        filterTable();
    });

    // Initialisation
    filterTable();
});