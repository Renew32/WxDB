document.addEventListener("DOMContentLoaded", function () {
    const tableRows = Array.from(document.querySelectorAll("#prestataireTable tr"));
    const filterVille = document.getElementById("filterVille");
    const filterType = document.getElementById("filterType");
    const searchInput = document.getElementById("searchInput");
    const noResults = document.getElementById("noResults");
    const entriesSelect = document.getElementById("entriesSelect");
    const paginationContainer = document.getElementById("pagination");

    let rowsPerPage = 15;
    let currentPage = 1;

    //filtre alphabetique
    function sortOptions(selectElement) {
        let options = Array.from(selectElement.options);

        // Garder l'option "Toutes les villes" en premier
        let firstOption = options.shift();

        // Trier par ordre alphabétique (insensible à la casse)
        options.sort((a, b) => a.text.localeCompare(b.text, "fr", { sensitivity: "base" }));

        // Réinsérer l'option en tête
        selectElement.innerHTML = "";
        selectElement.appendChild(firstOption);
        options.forEach(option => selectElement.appendChild(option));
    }

    sortOptions(filterVille);
    sortOptions(filterType);

    function filterTable() {
        let villeValue = filterVille.value.toLowerCase();
        let typeValue = filterType.value.toLowerCase();
        let searchValue = searchInput.value.toLowerCase();
        let filteredRows = [];

        // RECHERCHE
        tableRows.forEach(row => {
            let ville = row.querySelector(".ville").textContent.toLowerCase();
            let type = row.querySelector(".type").textContent.toLowerCase();
            let name = row.querySelector("td:first-child").textContent.toLowerCase();

            if ((villeValue === "" || ville.includes(villeValue)) &&
                (typeValue === "" || type.includes(typeValue)) &&
                (searchValue === "" || name.includes(searchValue))) {
                filteredRows.push(row);
            }
        });

        noResults.style.display = filteredRows.length === 0 ? "block" : "none";

        paginateTable(filteredRows);
    }

    function paginateTable(filteredRows) {
        let totalRows = filteredRows.length;
        let totalPages = Math.ceil(totalRows / rowsPerPage);
        if (currentPage > totalPages) currentPage = totalPages || 1;

        tableRows.forEach(row => row.style.display = "none");
        let start = (currentPage - 1) * rowsPerPage;
        let end = start + rowsPerPage;

        filteredRows.slice(start, end).forEach(row => row.style.display = "");

        updatePaginationControls(totalPages, filteredRows);
    }

    function updatePaginationControls(totalPages, filteredRows) {
        paginationContainer.innerHTML = "";
        let maxVisiblePages = 3;

        if (totalPages > 1) {
            let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
            let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

            if (endPage - startPage + 1 < maxVisiblePages) {
                startPage = Math.max(1, endPage - maxVisiblePages + 1);
            }


            // Ajouter "1" et "..." si besoin
            if (startPage > 1) {
                let firstPageBtn = document.createElement("button");
                firstPageBtn.textContent = "1";
                firstPageBtn.className = "page-btn";
                firstPageBtn.addEventListener("click", function () {
                    currentPage = 1;
                    paginateTable(filteredRows);
                });
                paginationContainer.appendChild(firstPageBtn);

                if (startPage > 2) {
                    let dots = document.createElement("span");
                    dots.textContent = "...";
                    dots.className = "page-btn disabled";
                    paginationContainer.appendChild(dots);
                }
            }

            // Afficher les numéros de pages actifs
            for (let i = startPage; i <= endPage; i++) {
                let btn = document.createElement("button");
                btn.textContent = i;
                btn.className = `page-btn ${i === currentPage ? "active" : ""}`;
                btn.addEventListener("click", function () {
                    currentPage = i;
                    paginateTable(filteredRows);
                });
                paginationContainer.appendChild(btn);
            }

            // Ajouter "..." et dernière page si besoin
            if (endPage < totalPages) {
                if (endPage < totalPages - 1) {
                    let dots = document.createElement("span");
                    dots.textContent = "...";
                    dots.className = "page-btn disabled";
                    paginationContainer.appendChild(dots);
                }

                let lastPageBtn = document.createElement("button");
                lastPageBtn.textContent = totalPages;
                lastPageBtn.className = "page-btn";
                lastPageBtn.addEventListener("click", function () {
                    currentPage = totalPages;
                    paginateTable(filteredRows);
                });
                paginationContainer.appendChild(lastPageBtn);
            }

            
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

    filterTable();
});