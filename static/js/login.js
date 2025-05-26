document.addEventListener("DOMContentLoaded", function () {
    async function connectAndSign() {
        const t = window.translations || {};
        const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
        const ncalayerClient = new NCALayerClient();

        document.getElementById("status").innerText = t.connecting || "Connecting...";

        try {
            await ncalayerClient.connect();
        } catch (error) {
            alert(`${t.connectionError || "Connection failed:"} ${error.toString()}`);
            return;
        }

        document.getElementById("status").innerText = t.connected || "Connected...";
        const groupid = document.getElementById("groupid").value;
        const documentBase64 = btoa(groupid);

        let signature;
        try {
            signature = await ncalayerClient.basicsSignCMS(
                NCALayerClient.basicsStorageAll,
                documentBase64,
                NCALayerClient.basicsCMSParamsAttached,
                NCALayerClient.basicsSignerSignAny
            );
        } catch (error) {
            alert((t.signatureError || "Signature error:") + " " + error.toString());
            return;
        }

        if (signature.includes("-----BEGIN CMS-----")) {
            signature = signature
                .replace("-----BEGIN CMS-----", "")
                .replace("-----END CMS-----", "")
                .replace(/\r?\n|\r/g, "")
                .trim();
        }

        document.getElementById("status").innerText = t.signatureReceived || "Sending...";

        const response = await fetch("/ru/login/ecp/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({
                signedData: signature,
                originalData: documentBase64
            })
        });

        const result = await response.json();

        document.getElementById("status").innerText = result.success
            ? (t.signatureValid || "Signature OK!")
            : (t.signatureInvalid || "Verification failed:") + " " + result.message;

        if (result.success && result.redirectUrl) {
            window.location.href = result.redirectUrl;
        }
    }

    const signButton = document.getElementById("signButton");
    if (signButton) {
        signButton.addEventListener("click", connectAndSign);
    }
});
