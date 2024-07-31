document.addEventListener('DOMContentLoaded', function() {
    let barChart = null;
    let pieChart = null;
    let doubleBarChart = null;
    let departmentDoubleBarChart = null;
   
  
    function createChart(ctx, type, data, options) {
        return new Chart(ctx, {
            type: type,
            data: data,
            options: options
        });
    }

    function destroyChart(chart) {
        if (chart) {
            chart.destroy();
        }
    }

    function updateDepartmentDoubleBarChart(data) {
        const ctx = document.getElementById('departmentDoubleBarChart').getContext('2d');
        destroyChart(departmentDoubleBarChart);
        departmentDoubleBarChart = createChart(ctx, 'bar', {
            labels: data.labels,
            datasets: [
                {
                    label: 'Total Feedback',
                    data: data.value_a,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Solved Feedback',
                    data: data.value_b,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        }, {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        });
    }


    function updateDoubleBarChart(data) {
        const ctx = document.getElementById('doubleBarChart').getContext('2d');
        destroyChart(doubleBarChart);
        doubleBarChart = createChart(ctx, 'bar', {
            labels: data.labels,
            datasets: [
                {
                    label: 'Total Feedback',
                    data: data.value_a,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Solved Feedback',
                    data: data.value_b,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        }, {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        });
    }

    function updateBarChart(data) {
        const ctx = document.getElementById('barChart').getContext('2d');
        destroyChart(barChart);
        barChart = createChart(ctx, 'bar', {
            labels: data.labels,
            datasets: [{
                label: 'Suggestions',
                data: data.values,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        }, {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        });
    }

    function updatePieChart(data) {
        const ctx = document.getElementById('pieChart').getContext('2d');
        destroyChart(pieChart);
        pieChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    datalabels: {
                        formatter: (value, ctx) => {
                            let sum = ctx.dataset.data.reduce((a, b) => a + b, 0);
                            let percentage = (value * 100 / sum).toFixed(2) + "%";
                            return percentage;
                        },
                        color: '#ffffff', // Corrected color code
                    }
                }
            },
            plugins: [ChartDataLabels] // Ensure the plugin is included
        });
    }
    

    function updateDepartmentName(name){
        document.getElementById('department-heading').textContent=name
    }

    function handleDropdownItemClicked(event) {
        const departmentId = event.target.getAttribute('department-clicked-id');
        const requestData = { department_id: departmentId };

        fetch('/organization/handle-department-action/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            updateBarChart(data.context.statistics);
            updatePieChart(data.context.statistics);
            updateDoubleBarChart(data.context.double_statistics);
            updateDepartmentName(data.context.department_name);
        })
        .catch(error => console.error('Error:', error));
    }

    document.querySelectorAll('.option-item').forEach(item => {
        item.addEventListener('click', handleDropdownItemClicked);
    });

    // Initialize charts with initial data
    updateDepartmentDoubleBarChart(initialDepartmentDoubleStatistics);
    updateBarChart(initialStatistics);
    updatePieChart(initialStatistics);
    updateDoubleBarChart(initialDoubleStatistics);
    updateDepartmentName(initialDepartmentName);
});
