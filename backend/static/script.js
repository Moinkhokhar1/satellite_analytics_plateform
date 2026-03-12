async function upload() {

    const fileInput = document.getElementById("imageUpload");

    if (fileInput.files.length === 0) {
        alert("Please select a file");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    document.getElementById("originalImg").src = data.original;
    document.getElementById("ndviImg").src = data.ndvi;
    document.getElementById("ndwiImg").src = data.ndwi;
    document.getElementById("classImg").src = data.classification;

    document.getElementById("ndviMin").innerText = data.ndvi.min.toFixed(3);
    document.getElementById("ndviMax").innerText = data.ndvi.max.toFixed(3);
    document.getElementById("ndviMean").innerText = data.ndvi.mean.toFixed(3);

}
