import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-stepper',
  standalone: true,
  imports: [],
  templateUrl: './stepper.component.html',
  styleUrl: './stepper.component.css'
})
export class StepperComponent implements OnInit{
  constructor() { }

  ngOnInit(): void {
    $(".step").click(function() {
      $(this).addClass("active").prevAll().addClass("active");
      $(this).nextAll().removeClass("active");
    });

    $(".step01").click(function() {
      $("#line-progress").css("width", "12%");
      $(".step1").addClass("active").siblings().removeClass("active");
    });

    $(".step02").click(function() {
      $("#line-progress").css("width", "52%");
      $(".step2").addClass("active").siblings().removeClass("active");
    });

    $(".step03").click(function() {
      $("#line-progress").css("width", "100%");
      $(".step3").addClass("active").siblings().removeClass("active");
    });
  }
}
