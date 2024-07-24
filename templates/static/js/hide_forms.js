function handleRadioChange() {
    const estate_for_sale = document.getElementById('estate_for_sale');
    const estate_on_auction = document.getElementById('estate_on_auction');
    const selectedValue = document.querySelector('input[name="category"]:checked').value;

    if (selectedValue === 'sell') {
        estate_for_sale.classList.remove('hidden');
        estate_on_auction.classList.add('hidden');
    } else if (selectedValue === 'auction') {
        estate_for_sale.classList.add('hidden');
        estate_on_auction.classList.remove('hidden');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('input[name="category"]').forEach((elem) => {
        elem.addEventListener('change', handleRadioChange);
    });
});