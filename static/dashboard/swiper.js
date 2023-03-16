if(document.querySelector('.quick_box')){
  var quick_box_swiper = new Swiper('.quick_box', {
    direction: 'horizontal',
    loop: true,
    speed:1500,
    autoplay:{
      delay:3000
    },
    pagination: {
      el: '.swiper-pagination',
    },
    navigation: {
      nextEl: '.quick_next',
      prevEl: '.quick_prev',
    },
  });
}

if(document.querySelector('.main_mid')){
  var mid_box_swiper = new Swiper('.main_mid', {
    direction: 'horizontal',
    loop: true,
    speed:2500,
    autoplay:{
      delay:3000
    },
    pagination: {
      el: '.swiper-pagination',
    },
  });
}

const mt_boxes = document.querySelectorAll('[id=mt_box]')
if(mt_boxes){
  for (let i = 0; i < mt_boxes.length; i++) {
    anime({
    targets: mt_boxes[i],
    opacity : [0,1],
    translateY: [-100,0],
    duration: parseInt(800) * parseInt(i+1),
    delay: parseInt(300) * parseInt(i+1)
    });
  }
}


