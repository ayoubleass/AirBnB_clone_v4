$(document).ready(() => {
  const amenityIds = [];
  const amenityNames = [];
  $('input[type=checkbox]').on('click', function () {
    const id = $(this).attr('data-id');
    const name = $(this).attr('data-name');
    if ($(this).prop('checked')) {
      amenityIds.push(id);
      amenityNames.push(name);
    } else {
      amenityIds.splice(amenityIds.indexOf(id), 1);
      amenityNames.splice(amenityNames.indexOf(name),1);
    }
    if (amenityNames.length !== 0) {
      $('div.amenities h4').text(amenityNames.join(', '));
    } else {
      $('div.amenities h4').html('&nbsp;');
    }
  });
});
