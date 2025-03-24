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

        // Toujours afficher la pagination, même avec une seule page
        for (let i = 1; i <= totalPages; i++) {
            let btn = document.createElement("button");
            btn.textContent = i;
            btn.className = `page-btn ${i === currentPage ? "active" : ""}`;
            btn.addEventListener("click", function () {
                currentPage = i;
                paginateTable(filteredRows);
            });
            paginationContainer.appendChild(btn);
        }

        // Ajouter "Précédent" et "Suivant" si plus d'une page
        if (totalPages > 1) {
            let prevBtn = document.createElement("button");
            prevBtn.textContent = "⬅ Précédent";
            prevBtn.className = "page-btn";
            prevBtn.disabled = currentPage === 1;
            prevBtn.addEventListener("click", function () {
                if (currentPage > 1) {
                    currentPage--;
                    paginateTable(filteredRows);
                }
            });

            let nextBtn = document.createElement("button");
            nextBtn.textContent = "Suivant ➡";
            nextBtn.className = "page-btn";
            nextBtn.disabled = currentPage === totalPages;
            nextBtn.addEventListener("click", function () {
                if (currentPage < totalPages) {
                    currentPage++;
                    paginateTable(filteredRows);
                }
            });

            paginationContainer.prepend(prevBtn);
            paginationContainer.appendChild(nextBtn);
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
    clearAll();
    

    
    
});