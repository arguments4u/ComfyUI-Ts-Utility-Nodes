const { app } = window.comfyAPI.app;

app.registerExtension({
	name: "TsLoadImageRGBClipSnapshot",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "TsLoadImageRGBClipSnapshot") {
			
			// When the node is executed we will be sent the input text, display this in the widget
			const onExecuted = nodeType.prototype.onExecuted;
			nodeType.prototype.onExecuted = function (message) {
				onExecuted?.apply(this, arguments);
				// do something
			};

		}
    },
	loadedGraphNode(node, _) {
		if (node.type === "TsLoadImageRGBClipSnapshot") {
			// do something
		}
	},
});

app.registerExtension({
	name: "TsLoadImageRGBAClipSnapshot",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "TsLoadImageRGBAClipSnapshot") {
			// When the node is executed we will be sent the input text, display this in the widget
			const onExecuted = nodeType.prototype.onExecuted;
			nodeType.prototype.onExecuted = function (message) {
				onExecuted?.apply(this, arguments);
				// do something
			};
		}
    },
	loadedGraphNode(node, _) {
		if (node.type === "TsLoadImageRGBAClipSnapshot") {
			// do something
		}
	},
});

//api.addEventListener("tk-path-to-image-from-clipboard", imagePathHandler);

