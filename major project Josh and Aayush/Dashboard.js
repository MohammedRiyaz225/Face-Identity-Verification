document.addEventListener('DOMContentLoaded', function() {
    // Toggle Sidebar Function
    function toggleSidebar() {
        var sidebar = document.getElementById('sidebar');
        var isOpen = sidebar.classList.contains('active');

        if (isOpen) {
            sidebar.classList.remove('active');
        } else {
            sidebar.classList.add('active');
        }
    }

    // Get the menu toggle button
    var menuToggle = document.getElementById('menu-toggle');

    // Add event listener for click event on the menu toggle button
    menuToggle.addEventListener('click', function() {
        toggleSidebar(); // Call the toggleSidebar function when the button is clicked
    });

    // Get the canvas element
    var ctx = document.getElementById('myChart').getContext('2d');

    // Create the chart
    var myChart = new Chart(ctx, {
        type: 'bar', // Specify the chart type
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'], // Labels for X-axis
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3], // Data values
                backgroundColor: [ // Colors for each bar
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [ // Border colors for each bar
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1 // Border width for each bar
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true // Start Y-axis from zero
                }
            }
        }
    });
});
