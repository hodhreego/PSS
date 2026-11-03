// Clique no ícone da extensão abre o painel lateral.
chrome.runtime.onInstalled.addListener(async () => {
  try {
    await chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
  } catch (e) {
    console.error("Postador: não consegui configurar o painel lateral", e);
  }
});
