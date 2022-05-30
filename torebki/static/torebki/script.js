let paperSelect = document.getElementById('paper');
let overprintSelect = document.getElementById('overprint');
let laminateSelect = document.getElementById('laminate');
let colorsSelect = document.getElementById('colors');
let dimensionsSelect = document.getElementById('dimensions');
let handleTypeDiv = document.getElementById('handle-type-options');
let customDimensionsCheckbox = document.getElementById(
  'custom-dimensions-checkbox'
);
let customDimensionsContainer = document.getElementById('custom-dimensions');
let customWidth = document.getElementById('custom-width');
let customHeight = document.getElementById('custom-height');
let customDepth = document.getElementById('custom-depth');

let paperGrammage = document.getElementById('paper-grammage');
let paperSize = document.getElementById('paper-size');
let paperType = document.getElementById('paper-type');

let bagForm = document.getElementById('form');
let priceSpan = document.getElementById('price-value');
let paperPriceSpan = document.getElementById('paper-price');
let overprintPriceSpan = document.getElementById('overprint-price');
let laminatePriceSpan = document.getElementById('laminate-price');
let colorPriceSpan = document.getElementById('color-price');
let handleTypePriceSpan = document.getElementById('handle-type-price');

for (paper of data.papers) {
  paperSelect.appendChild(new Option(`#${paper.id}`, paper.id));
}
for (overprint of data.overprints) {
  overprintSelect.appendChild(
    new Option(overprint.overprint_type, overprint.id)
  );
}
for (laminate of data.laminates) {
  laminateSelect.appendChild(new Option(laminate.laminate_type, laminate.id));
}
for (color of data.colors) {
  colorsSelect.appendChild(new Option(color.colors_num, color.id));
}
for (handleType of data.handleTypes) {
  let handleTypeRadio = document.createElement('input');
  handleTypeRadio.type = 'radio';
  handleTypeRadio.id = handleType.id;
  handleTypeRadio.name = 'handle_type';
  handleTypeRadio.value = handleType.id;
  handleTypeRadio.setAttribute('required', 'required');
  handleTypeRadio.setAttribute('checked', 'checked');

  let handleTypeLabel = document.createElement('label');
  handleTypeLabel.htmlFor = handleTypeRadio.id;
  handleTypeLabel.innerText = handleType.handle_type;

  handleTypeDiv.appendChild(handleTypeRadio);
  handleTypeDiv.appendChild(handleTypeLabel);
  handleTypeDiv.appendChild(document.createElement('br'));
}
for (dimension of data.bagDimensions) {
  dimensionsSelect.appendChild(
    new Option(
      `${dimension.width}cm x ${dimension.height}cm x ${dimension.depth}cm`,
      dimension.id
    )
  );
}

customDimensionsCheckbox.onchange = (e) => {
  if (e.currentTarget.checked) {
    dimensionsSelect.setAttribute('disabled', 'disabled');
    customDimensionsContainer.removeAttribute('hidden');
    customHeight.removeAttribute('disabled');
    customDepth.removeAttribute('disabled');
    customWidth.removeAttribute('disabled');
  } else {
    customDimensionsContainer.setAttribute('hidden', 'hidden');
    dimensionsSelect.removeAttribute('disabled');
    customHeight.setAttribute('disabled', 'disabled');
    customDepth.setAttribute('disabled', 'disabled');
    customWidth.setAttribute('disabled', 'disabled');
  }
};
const getPaperInfo = (e) => {
  let paperInfo = data.papers.find(
    (paper) => paper.id == e.currentTarget.value
  );
  paperGrammage.innerText = paperInfo.grammage;
  paperSize.innerText = paperInfo.size;
  paperType.innerText = paperInfo.paper_type;
};
paperSelect.onchange = getPaperInfo;
paperSelect.dispatchEvent(new Event('change'));

bagForm.oninput = (e) => {
  let handleTypePrice = data.handleTypes.find(
    (handleType) =>
      handleType.id ==
      Array.from(document.querySelectorAll('#handle-type-options>input')).find(
        (radio) => radio.checked
      ).value
  ).price;
  let price =
    data.papers.find((paper) => paper.id == paperSelect.value).price +
    data.colors.find((color) => color.id == colorsSelect.value).price +
    data.laminates.find((laminate) => laminate.id == laminateSelect.value)
      .price +
    data.overprints.find((overprint) => overprint.id == overprintSelect.value)
      .price +
    handleTypePrice;
  priceSpan.innerText = `${price.toFixed(2)} zł`;
  paperPriceSpan.innerText = `+${data.papers
    .find((paper) => paper.id == paperSelect.value)
    .price.toFixed(2)} zł`;
  overprintPriceSpan.innerText = `+${data.overprints
    .find((overprint) => overprint.id == overprintSelect.value)
    .price.toFixed(2)} zł`;
  laminatePriceSpan.innerText = `+${data.laminates
    .find((laminate) => laminate.id == laminateSelect.value)
    .price.toFixed(2)} zł`;
  colorPriceSpan.innerText = `+${data.colors
    .find((color) => color.id == colorsSelect.value)
    .price.toFixed(2)} zł`;
  handleTypePriceSpan.innerText = `+${handleTypePrice.toFixed(2)} zł`;
};
bagForm.dispatchEvent(new Event('input'));
