document.addEventListener('DOMContentLoaded', function() {
  var navItems = document.querySelectorAll('.nav-item');
  var contentDivs = document.querySelectorAll('#content-container > div');
  
  contentDivs.forEach(function(div) {
    if (div.id !== 'smartphone') {
      div.style.display = 'none';
    }
  });

  var defaultNavItem = document.getElementById('smartphone');
  defaultNavItem.click();

  navItems.forEach(function(navItem) {
    navItem.addEventListener('click', function() {
      var id = navItem.id;

      contentDivs.forEach(function(div) {
        if (div.id === id) {
          div.style.display = 'block';
        } else {
          div.style.display = 'none';
        }
      });

      navItems.forEach(function(item) {
        if (item === navItem) {
          item.classList.add('selected');
        } else {
          item.classList.remove('selected');
        }
      });
    });
  });
});


  function updateGenerationOptions(brandSelectId, generationSelectId, intelGenerations, amdGenerations) {
    var brandSelect = document.getElementById(brandSelectId);
    var generationSelect = document.getElementById(generationSelectId);

    brandSelect.addEventListener('change', function() {
      generationSelect.innerHTML = ''; 

      var selectedBrand = this.value;

      var generations = [];
      switch (selectedBrand) {
        case 'Intel':
          generations = intelGenerations;
          break;
        case 'AMD':
          generations = amdGenerations;
          break;
        case 'Snapdragon':
          generations = ['Qualcomm Snapdragon 888','Snapdragon 898 (4 nm)', 'Snapdragon 888 (5 nm)', 'Snapdragon 870 (7 nm)','Snapdragon 780G (5 nm)','Snapdragon 765G (7 nm)','Snapdragon 750G (8 nm)','Snapdragon 732G (8 nm)','Snapdragon 730G (8 nm)'];
          break;
        case 'Google Tensor':
          generations = ['Google Tensor (2021) Dual-core Cortex-X1(2.80 GHz)','Google Tensor G2 (2022) Dual-core Cortex-X1(2.85 GHz)','Google Tensor G3 (2023) Dual-core Cortex-X1(2.90 GHz)'];
          break;
        case 'Apple A':
          generations = ['A15 Bionic Hexa-core(6 GHz)', 'Apple A17 Pro (3nm)', 'Apple A12 Bionic (5 GHz)','Apple A14 Bionic (6 GHz)','Apple A16 Bionic(4nm)','Apple A10 Fusion Quad-core(2.34 GHz)','Apple A8 Dual-core(1.4 GHz'];
          break;
        default:
          generations = [];
      }
      generations.forEach(function(gen) {
        var option = document.createElement('option');
        option.text = gen;
        option.value = gen; 
        generationSelect.add(option);
      });

      if (generations.length > 0) {
        generationSelect.value = generations[0]; 
      } else {
        generationSelect.value = ''; 
      }
    });
  }

  var intelGenerations = ['i7 12th Gen', 'i7 10th Gen', 'i5 12th Gen', 'i5 10th Gen', 'i3 12th Gen', 'i3 10th Gen', 'i7 11th Gen', 'i3 11th Gen', 'i5 11th Gen', 'i7 9th Gen'];
  var amdGenerations = ['Ryzen 5 Octa Core', 'Ryzen 4 Octa Core', 'Ryzen 3 Octa Core', 'Ryzen 5 Hexa Core', 'Ryzen 4 Hexa Core', 'Ryzen 3 Hexa Core'];

  updateGenerationOptions('brandSelect', 'generationSelect', intelGenerations, amdGenerations);

  updateGenerationOptions('brandSelect1', 'generationSelect1', intelGenerations, amdGenerations);

  updateGenerationOptions('brandSelect2', 'generationSelect2', intelGenerations, amdGenerations);

  const uploadButtons = document.querySelectorAll('.uploadFile');
  const fileListContainers = document.querySelectorAll('.photoList');

  uploadButtons.forEach((button, index) => {
    button.addEventListener('change', function (event) {
      const fileListContainer = fileListContainers[index];

      const files = event.target.files;

      for (let i = 0; i < files.length; i++) {
        const file = files[i];

        if (!file.type.startsWith('image/')) {
          alert('Please upload only image files.');
          continue;
        }

        const reader = new FileReader();

        reader.onload = function (e) {
          const img = new Image();
          img.src = e.target.result;
          img.width = 100; 

          const deleteIcon = document.createElement('i');
          deleteIcon.classList.add('bi', 'bi-x-circle-fill', 'text-danger', 'fs-5', 'position-absolute', 'top-0', 'end-0', 'm-2');
          deleteIcon.style.cursor = 'pointer';

          deleteIcon.addEventListener('click', function () {
            fileListContainer.removeChild(img.parentNode);
          });

          const imageContainer = document.createElement('div');
          imageContainer.classList.add('position-relative');
          imageContainer.appendChild(img);
          imageContainer.appendChild(deleteIcon);

          fileListContainer.appendChild(imageContainer);
        };

        reader.readAsDataURL(file);
      }
    });
  });








  
