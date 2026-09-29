#!/usr/bin/env bash
#
# iLuno - cria as Issues da Onda 1 no GitHub a partir do BACKLOG.xlsx
#
# Pre-requisitos:
#   1. GitHub CLI instalado:  https://cli.github.com
#   2. Autenticado:           gh auth login
#   3. Executar de dentro do diretorio do repositorio clonado,
#      ou definir REPO abaixo (ex.: REPO="usuario/iluno").
#
# Uso:
#   chmod +x criar_issues_onda1.sh
#   ./criar_issues_onda1.sh              # cria as issues
#   ./criar_issues_onda1.sh --dry-run    # so mostra o que seria criado
#
# As issues sao criadas na ordem T01..T08, T15, T17, T16, de modo que a
# numeracao do GitHub (#1..#8) bata com a coluna "Issue #" da planilha.
# T15, T16 e T17 ficam com #9, #10 e #11 - anote na planilha depois.

set -euo pipefail

REPO=""            # ex.: "lucca/iluno". Vazio = usa o repositorio da pasta atual.
DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

gh_args=()
[[ -n "$REPO" ]] && gh_args+=(--repo "$REPO")

# ---------------------------------------------------------------- labels
# Labels usadas: tipo (Backend/Frontend/DevOps), onda e estimativa.
criar_label() {
  local nome="$1" cor="$2" desc="$3"
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] label: $nome"
    return
  fi
  gh label create "$nome" --color "$cor" --description "$desc" "${gh_args[@]}" 2>/dev/null \
    || echo "  label '$nome' ja existe, seguindo"
}

echo "== Criando labels =="
criar_label "backend"    "1D76DB" "Tarefa de backend"
criar_label "frontend"   "0E8A16" "Tarefa de frontend"
criar_label "devops"     "5319E7" "Infraestrutura e configuracao"
criar_label "onda-1"     "FBCA04" "Onda 1 do Sequenciador"
criar_label "estimativa-P" "C2E0C6" "P = ate 2h"
criar_label "estimativa-M" "FEF2C0" "M = 2 a 6h"

# ---------------------------------------------------------------- issues
criar_issue() {
  local id="$1" func="$2" tipo="$3" est="$4" titulo="$5"
  local corpo
  corpo=$(cat <<EOF
**Tarefa:** $id
**Funcionalidade de origem:** $func
**Onda:** 1
**Tipo:** $tipo
**Estimativa:** $est

$titulo

---
Rastreabilidade: esta Issue corresponde a linha $id do BACKLOG.xlsx (raiz do repositorio).
EOF
)
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] [$id] $titulo"
    return
  fi
  gh issue create \
    --title "[$id] $titulo" \
    --body "$corpo" \
    --label "$(echo "$tipo" | tr '[:upper:]' '[:lower:]')" \
    --label "onda-1" \
    --label "estimativa-$est" \
    "${gh_args[@]}"
}

echo
echo "== Criando Issues da Onda 1 =="

criar_issue "T01" "F01" "Backend"  "P" "Criar modelo de usuário no Firestore e habilitar o Firebase Authentication"
criar_issue "T02" "F01" "Frontend" "P" "Desenvolver formulário de cadastro em React com validação"
criar_issue "T03" "F01" "Frontend" "P" "Criar tela de perfil do usuário em React"
criar_issue "T04" "F02" "Backend"  "P" "Criar modelo de disciplina no Firestore"
criar_issue "T05" "F02" "Backend"  "M" "Criar endpoint de busca de disciplina por nome na API Python (FastAPI)"
criar_issue "T06" "F03" "Backend"  "M" "Definir modelo de tópicos de avaliação no Firestore"
criar_issue "T07" "F03" "Frontend" "M" "Exibir informações e tópicos da disciplina na tela em React"
criar_issue "T08" "F03" "DevOps"   "P" "Configurar as regras de segurança do Firestore para envio de avaliações"
criar_issue "T15" "F01" "DevOps"   "P" "Criar projeto no Firebase e configurar Authentication e Firestore"
criar_issue "T16" "F01" "DevOps"   "P" "Conectar o repositório GitHub à Vercel e configurar o deploy contínuo"
criar_issue "T17" "F02" "Backend"  "M" "Inicializar a API em Python (FastAPI) e publicá-la na Vercel"

echo
echo "Pronto. Confira com: gh issue list ${REPO:+--repo $REPO}"
echo "Depois preencha a coluna 'Issue #' do BACKLOG.xlsx para T15, T16 e T17"
echo "e faca o segundo commit da planilha."
