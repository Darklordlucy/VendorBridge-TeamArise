// Chart.js Configuration Helpers for VendorBridge Reports

export function initSpendTrendsChart(canvasId, labels, dataPoints) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels || ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Monthly Spend (₹)',
                data: dataPoints || [120000, 150000, 80000, 220000, 190000, 324000],
                backgroundColor: 'rgba(0, 70, 67, 0.85)', // Cyprus with opacity
                borderColor: '#004643',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 70, 67, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

export function initCategoryBreakdownChart(canvasId, categories, dataPoints) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: categories || ['IT Hardware', 'Office Supplies', 'Furniture', 'Logistics'],
            datasets: [{
                data: dataPoints || [55, 15, 20, 10],
                backgroundColor: [
                    '#004643', // Cyprus
                    '#ABD1C6', // Mint
                    '#F9BC60', // Yellow accent
                    '#E4DFD5'  // Sand dark
                ],
                borderWidth: 2,
                borderColor: '#FFFFFF'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        padding: 16
                    }
                }
            }
        }
    });
}
