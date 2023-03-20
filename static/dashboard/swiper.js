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
  quick_box_swiper.el.onmouseenter =()=>{
    quick_box_swiper.autoplay.stop()
  }
  quick_box_swiper.el.onmouseleave =()=>{
    quick_box_swiper.autoplay.start()
  }
}

if(document.querySelector('.main_mid')){
  var mid_box_swiper = new Swiper('.main_mid', {
    direction: 'horizontal',
    loop: true,
    speed:2500,
    autoplay:{
      delay:3000
    },
    // pagination: {
    //   el: '.swiper-pagination',
    // },
  });
  mid_box_swiper.el.onmouseenter =()=>{
    mid_box_swiper.autoplay.stop()
  }
  mid_box_swiper.el.onmouseleave =()=>{
    mid_box_swiper.autoplay.start()
  }
}

if(document.querySelector('.ad_swiper')){
  var mid_box_swiper = new Swiper('.ad_swiper', {
    direction: 'horizontal',
    loop: true,
    speed:2500,
    autoplay:{
      delay:3000
    },
    disableOnInteraction:true,
    // pagination: {
    //   el: '.swiper-pagination',
    // },
  });
  mid_box_swiper.el.onmouseenter =()=>{
    mid_box_swiper.autoplay.stop()
  }
  mid_box_swiper.el.onmouseleave =()=>{
    mid_box_swiper.autoplay.start()
  }
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


