$(document).ready(function() {
    $('.addStudentScore').click(function() {
        var id = $(this).data('id');
        var firstname = $(this).data('firstname');
        var lastname = $(this).data('lastname');
        $('#id').text(id);
        $('#studentid').text(id);
        $('#firstname').text(firstname);
        $('#lastname').text(lastname);
    });
});


const addStudentScores = document.querySelectorAll(".addStudentScore");
addStudentScores.forEach((button) => {
    button.addEventListener('click', () => {
        const notIncludedKeys = ['bsTarget', 'bsToggle'];
        const datasets = button.dataset;
        Object.entries(datasets).forEach(([key, value]) => {
            if (notIncludedKeys.includes(key)) {
                return;
            }
            console.log(`${key}: ${value}`)
            const input = document.querySelector(`input[name="${key}"]`);
            console.log(input)
            if (input) {
                input.value = value;
            }
        })
    });
})
