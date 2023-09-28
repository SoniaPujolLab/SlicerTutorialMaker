const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  const htmlFile = 'output_tutorial.html'; // Reemplaza con el nombre de tu archivo HTML

  await page.goto(`file://${__dirname}/${htmlFile}`, {
    waitUntil: 'networkidle0',
  });

  const pdfFile = 'output_tutorial.pdf'; // Nombre del archivo PDF de salida
  await page.pdf({ path: pdfFile, format: 'A4' });

  await browser.close();
  console.log(`PDF generado: ${pdfFile}`);
})();
