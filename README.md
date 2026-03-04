### **Resumo das Atualizações**

* **Expansão da Interface (UI):** Implementação de uma quarta variável de controle (`extra_var`) e seu respectivo campo de entrada no layout principal para capturar informações complementares (ex: RQE, especialidade ou setor).
* **Lógica de Renderização Dinâmica:** O sistema de desenho agora utiliza uma lista filtrada (`textos_para_exibir`) que ignora campos em branco. Isso evita que linhas vazias sejam geradas na imagem caso o usuário não preencha o campo extra.
* **Ajuste de Fluxo de Desenho:** Substituição das coordenadas fixas de texto por um loop de iteração. Isso permite que as informações (de 3 a 4 linhas) sejam centralizadas e empilhadas automaticamente abaixo da assinatura.
* **Otimização de Espaçamento:** No modo de **Prescrição**, o intervalo entre as linhas foi ajustado de `10` para `12` unidades para garantir a legibilidade das informações adicionais sem sobreposição.
