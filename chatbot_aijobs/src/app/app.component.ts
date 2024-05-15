import { Component, ElementRef, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'chatGTPClient';
  loadinterval: any;
  bot = './assets/bot.svg';
  user = './assets/user.svg';
  labelUsername = 'Você';
  labelBotname = 'Chatbot';
  form:any;
  container:any;
  isVisible:boolean = true;
  listFAQ = [
    { "text": "Qual a quantidade de vagas disponíveis hoje?", "score": 15 },
    { "text": "Quais são as vagas de regime home office?", "score": 10 },
    { "text": "Quais são as vagas que possuem Gympass?", "score": 7 },
    { "text": "Qual a vaga que oferece os melhores benefícios?", "score": 2 }
  ]

  @Output() updatePromptEvent = new EventEmitter<string>();

  constructor(private elementref: ElementRef) {}

  ngAfterViewInit(){
    this.form = this.elementref.nativeElement.querySelector('form');
    this.form.addEventListener('submit', this.handlesubmit);
    this.form.addEventListener('keyup', (e: any) => { 
      if (e.keycode === 13){
        this.handlesubmit(e);
      }
    });
    this.container = this.elementref.nativeElement.querySelector('#container');
    this.listFAQ.sort((a, b) => b.score - a.score);
  }

  submitFAQ(pergunta: string): void {
    const textarea = this.form.querySelector('textarea');
    if (textarea != null) {
      textarea.value = pergunta;
    }

    this.handlesubmit({ preventDefault: () => {} });
  }

  loader(element: any){
    element.textContent = '';
    this.loadinterval = setInterval(() => {
      element.textContent += '.';
      if (element.textContent === '....'){
          element.textContent = '';
      }
    }, 300)
  }

  typetext(element:any, text:any){
    let index = 0;
    if (element) {
      // Adiciona o novo código HTML à div existente
      element.innerHTML = `<b>${this.labelBotname}</b><br>${element.innerHTML}`;
    }
    let interval = setInterval(() => {
      if (index < text.length){
        element.innerHTML += text.charAt(index);
        index++;
      }
      else {
        clearInterval(interval);
      }
    }, 20)
  }

  generateUniqueId(){
    const timestamp = Date.now();
    const rnNumber = Math.random();
    const hex = rnNumber.toString(16);
    return `id-${timestamp}-${hex}`;
  }

  stripes(ai: any, value:any, uniqueId: any){
    return(
      `
      <div class= "wrapper ${ai && 'ai'}">
        <div class="chat">
          <div class="profile">
            <img src="${ai ? this.bot : this.user}"/>
          </div>
          <div class="message" id=${uniqueId}><b>${ai ? this.labelBotname : this.labelUsername}</b><br>${value}</div>
          
        </div>
      </div>
      `
    )
  }

  handlesubmit = async(e: any) => {
    this.isVisible = false
    e.preventDefault();

    const data = new FormData(this.form ?? undefined);

    if (this.container != null) {
      this.container.innerHTML += this.stripes(false, data.get('prompt'), null)
    }

    const uniqueId = this.generateUniqueId();

    if (this.container != null){
      this.container.innerHTML += this.stripes(true, " ", uniqueId);
      this.container.scrollTop = this.container?.scrollHeight;
    }

    if (this.form != null) {
      const textarea = this.form.querySelector('textarea');
      if (textarea != null) {
        textarea.value = '';
      }
    }

    const messageDiv = document.getElementById(uniqueId);
    this.loader(messageDiv);

    const response = await fetch("http://172.16.20.27:5006/api/question", {
      method: 'POST',
      headers:{
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({

        question: data.get('prompt'),
        user_id: "user",
        temperature: 0
      })
    })

    clearInterval(this.loadinterval);

    if (messageDiv != null){
      messageDiv.innerHTML = '';
    }

    if (response.ok){
      const data = await response.json();
      this.typetext(messageDiv, data.response);
    }else {
      const err = await response.text();
      if (messageDiv != null){
        messageDiv.innerHTML = 'Something went wrong';
        alert(err);
      }
    }
  }

}
