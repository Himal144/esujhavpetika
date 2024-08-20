
// Code for generating the qr code for the parent and if the child is logged in 
// Generate QR code for the main organization
new QRCode(document.getElementById("qr-code"), {
    text: url,
    width: 140,
    height: 140,
});

//Code for downloading the qr of child when child login and parent qr when parent login
document.querySelector('#qr-download-btn').addEventListener('click', function () {
        const qrCodeCanvas = document.querySelector(`#qr-code canvas`);
        if (qrCodeCanvas) {
            // Load the template HTML
            fetch('/organization/qr-templates/')
                .then(response => response.text())
                .then(templateHtml => {
                    const pdfContent = document.createElement('div');
                    pdfContent.innerHTML = templateHtml;

                    // Populate the template with dynamic data

                    pdfContent.querySelector('#org-name').textContent = organization;
                    pdfContent.querySelector('#qr-code-img').src = qrCodeCanvas.toDataURL("image/png");

                    // Convert the content to PDF
                    html2pdf(pdfContent, {
                        margin: [0, 0, 0, 0],
                        filename: `qr-code-${organization}.pdf`,
                        image: { type: 'jpeg', quality: 0.98 },
                        html2canvas: { scale: 2 },
                        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
                    });
                })
                .catch(error => console.error('Error loading template:', error));
        }
    });
    // Adjust QR code canvas size dynamically based on container
function resizeQrCodeCanvas() {
    const qrCodeContainers = document.querySelectorAll('.qr-code');
    qrCodeContainers.forEach(container => {
        const canvas = container.querySelector('canvas');
        if (canvas) {
            // Adjust canvas width based on container size
            const containerWidth = container.clientWidth;
            if (containerWidth < 140) {
                canvas.style.width = `${containerWidth}px`;
                canvas.style.height = `${containerWidth}px`;
            }
        }
    });
}

// Call the resize function after the QR codes are generated
resizeQrCodeCanvas();

// Add an event listener to resize the canvas on window resize
window.addEventListener('resize', resizeQrCodeCanvas);










// Code for generating the QR code if the parent organization has departments
if (childOrganizations!=null) {
    childOrganizations.forEach((child, index) => {
        const qrCodeContainer = document.getElementById(`qr-code-${index + 1}`);
        new QRCode(qrCodeContainer, {
            text: child.url,
            width: 140,
            height: 140,
        });
    });

    // code for the downloading the qr code for child organization qr when parent log in

document.querySelectorAll('.qr-download-btn').forEach(button => {
    button.addEventListener('click', function () {
        const counter = this.getAttribute('data-counter');
        const qrCodeCanvas = document.querySelector(`#qr-code-${counter} canvas`);
        if (qrCodeCanvas) {
            // Load the template HTML
            fetch('/organization/qr-templates/')
                .then(response => response.text())
                .then(templateHtml => {
                    const pdfContent = document.createElement('div');
                    pdfContent.innerHTML = templateHtml;

                    // Populate the template with dynamic data

                    alert(childOrganizations[counter - 1].name)
                    pdfContent.querySelector('#org-name').textContent = childOrganizations[counter - 1].name;
                    pdfContent.querySelector('#qr-code-img').src = qrCodeCanvas.toDataURL("image/png");

                    // Convert the content to PDF
                    html2pdf(pdfContent, {
                        margin: [0, 0, 0, 0],
                        filename: `qr-code-${childOrganizations[counter - 1].name}.pdf`,
                        image: { type: 'jpeg', quality: 0.98 },
                        html2canvas: { scale: 2 },
                        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
                    });
                })
                .catch(error => console.error('Error loading template:', error));
        }
    });
});
}


