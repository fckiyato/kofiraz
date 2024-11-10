document.addEventListener('DOMContentLoaded', function () {
    var dropdown = document.getElementById('userDropdown');
    var menu = dropdown.nextElementSibling;

    // Toggle the dropdown on button click
    dropdown.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent this click from closing the dropdown
        menu.classList.toggle('show');
    });

    // Close the dropdown if clicked outside of it
    document.addEventListener('click', function(event) {
        if (!dropdown.contains(event.target)) {
            menu.classList.remove('show');
        }
    });
});






document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("messageModal");
    const closeModal = document.getElementById("closeModal");
    const okButton = document.getElementById("okButton");

    if (modal) {
        // Show the modal
        modal.style.display = "flex"; // Use "flex" to center the modal content

        // Close the modal when clicking the close button
        closeModal.onclick = function () {
            modal.style.display = "none";
        };

        // Close the modal when clicking the OK button
        okButton.onclick = function () {
            modal.style.display = "none";
        };

        // Close the modal when clicking outside of the modal content
        window.onclick = function (event) {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };
    }
});
