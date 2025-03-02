/*

```javascript
*/


async function exportSelectionAsImage() {
    const eaAPI = ea.getExcalidrawAPI();
    if (!eaAPI) {
        new Notice("Excalidraw não encontrado!");
        return;
    }

    const selectedElements = ea.getViewSelectedElements();
    if (selectedElements.length === 0) {
        new Notice("Nenhum elemento selecionado!");
        return;
    }


	let xMean = 0;
	let yMean = 0;
	let widthMean = 0;
	let heightMean = 0;
	for(const element of selectedElements){
		xMean += element.x
		yMean += element.y
		widthMean += element.width
		heightMean += element.height
	}
	

	xMean = xMean / selectedElements.length
	yMean = yMean / selectedElements.length
	
	heightMean = heightMean / selectedElements.length
	widthMean  = widthMean  / selectedElements.length

    const params = {
        elements: selectedElements,
        appState: eaAPI.getAppState(),
        exportPadding: 5
    };

    const canvas = await this.ExcalidrawLib.exportToCanvas(params);
    
    canvas.toBlob(async (blob) => {
        if (!blob) {
            new Notice("Erro ao gerar imagem!");
            return;
        }

        const formData = new FormData();
        formData.append("file", blob, "desenho.png");

        try {
            const response = await fetch("http://localhost:8000/ocr", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Erro na requisição: ${response.statusText}`);
            }

            const result = await response.json();
        

            new Notice("Imagem enviada com sucesso!");
            let textoCompleto = "";
		    for(const textoDetectado of result.text_detected){
			   textoCompleto += textoDetectado.text 
		    }
		    
            ea.addText(xMean,yMean,textoCompleto,{width:widthMean,height:heightMean})
			ea.addElementsToView(true)
			ea.deleteViewElements(selectedElements)
        } catch (error) {
            console.error("Erro ao enviar imagem:", error);
            new Notice("Erro ao enviar a imagem para o servidor!");
        }
    }, "image/png");
}

exportSelectionAsImage();
