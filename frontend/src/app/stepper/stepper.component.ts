import { Component, OnInit, AfterViewInit, ElementRef } from '@angular/core';
import { Router } from '@angular/router';
import {CommonModule} from "@angular/common";

@Component({
  selector: 'app-stepper',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './stepper.component.html',
  styleUrl: './stepper.component.css'
})
export class StepperComponent implements OnInit, AfterViewInit {
  algorithms = [
    { name: 'Algorithm 1', description: 'Description of Algorithm 1' },
    { name: 'Algorithm 2', description: 'Description of Algorithm 2' },
    { name: 'Algorithm 3', description: 'Description of Algorithm 3' },
  ];

  pricingmodels = [
    { name: 'Pricing model 1', description: 'Description of Pricing model 1' },
    { name: 'Pricing model 2', description: 'Description of Pricing model 2' },
    { name: 'Pricing model 3', description: 'Description of Pricing model 3' },
  ];

  twinworlds = [
    { name: 'Twin world 1', description: 'Description of Twin world 1' },
    { name: 'Twin world 2', description: 'Description of Twin world 2' },
    { name: 'Twin world 3', description: 'Description of Twin world 3' },
  ];

  currentDescription: string = '';

  constructor(private elementRef: ElementRef, private router: Router) { }

  ngOnInit(): void {

  }

  changeDescription(description: string) {
      this.currentDescription = description;
  }

  resetDescriptions() {
    this.currentDescription = '';
  }

  private activateStep(stepNumber: number) {
    $('.step').removeClass('active');
    $(`.step0${stepNumber}`).addClass('active');
    let progressBarWidth = '0%';
    switch (stepNumber) {
      case 1:
        progressBarWidth = '12%';
        break;
      case 2:
        progressBarWidth = '52%';
        break;
      case 3:
        progressBarWidth = '100%';
        break;
    }
    $('#line-progress').css('width', progressBarWidth);
    $('.section-content').removeClass('active');
    $(`.section-content.step${stepNumber}`).addClass('active');
  }

  ngAfterViewInit() {
    const self = this;

    this.elementRef.nativeElement.ownerDocument
      .body.style.backgroundColor = '#1e1e2d';

    $(".step").click(function() {
      $(this).addClass("active").prevAll().addClass("active");
      $(this).nextAll().removeClass("active");
      self.resetDescriptions();
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

    $(".step1 .item").click(function() {
      self.activateStep(2);
    });

    $(".step2 .item").click(function() {
      self.activateStep(3);
    });

    $(".step3 .item").click(function() {
      self.router.navigate(['/sl']);
    });
  }
}
