document.addEventListener('DOMContentLoaded', function() {
    DeleteAlert();
});

function DeleteAlert() {
    const deleteLinks = document.querySelectorAll('a.delete');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            Swal.fire({
                title: '¿Estás seguro?',
                text: "No podrás revertir esta acción!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Si, eliminar!',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.value) {
                    window.location.href = url;
                }
            });
        });
    });
}