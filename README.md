# 🖋️ Gerador de Assinaturas Profissionais

Esta é uma interface gráfica simples em Python que gera automaticamente **imagens com assinaturas personalizadas** para documentos como *prescrição* e *evolução*, com base em informações fornecidas pelo usuário (nome, profissão e número de conselho). Ideal para uso em ambientes de saúde ou administrativos.

---

## 🧩 Funcionalidades

- Interface intuitiva em **Tkinter**.
- Geração de duas imagens:
  - **Evolução** (268×85 px)
  - **Prescrição** (344×143 px)
- Redimensionamento automático da imagem de assinatura para um **espaço fixo definido**.
- Saída final no formato `.bmp`, pronta para uso institucional.

---

## 📷 Exemplo de uso

1. O usuário seleciona uma imagem da sua assinatura (em `.png`, `.jpg`, etc.).
2. Preenche os dados:
   - Nome completo
   - Número do conselho
   - Profissão
3. Gera a imagem de prescrição ou evolução.
4. As imagens são salvas automaticamente dentro de uma pasta com o nome sanitizado do profissional:


---

## 🚀 Como executar

### 1. Instale as dependências

```bash
pip install pillow

