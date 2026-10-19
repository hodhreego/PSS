# Site do Prof. Rodrigo Gonçalves Pereira

Página única (HTML, CSS e JavaScript no mesmo arquivo), pronta para publicar em qualquer hospedagem estática
(por exemplo GitHub Pages: coloque `index.html` na raiz do repositório e ative Pages).

- `index.html`: o site completo, com a foto e os sons embutidos.
- `fonte-sem-foto.html`: o mesmo código sem a foto embutida (o texto `__FOTO__` marca onde ela entra).
- `sons/`: os sons de moeda usados no botão de serviços, com origem e licenças em `sons/LICENCAS.md`.

## O que ajustar antes de publicar

No começo do `<script>` ficam as configurações: valor da hora, piso, percentuais de acréscimo, agenda (dias,
turnos e horários), lista de serviços, períodos de renovação e condições do contrato.

A constante `PAGE_URL` guarda o endereço da página. Os links de orçamento enviados pelos contratantes são
`PAGE_URL` + `#o7.` + o código do orçamento. Troque o valor quando publicar em outro endereço.

Não coloque no site o CPF nem o endereço do certificado do MEI.
