#!/bin/bash
# 健康檢查腳本
# 使用方法: ./health_check.sh

set -e

# 顏色輸出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  Project Observer 健康檢查${NC}"
echo -e "${BLUE}  $(date)${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# 檢查結果統計
CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNED=0

# 函數：檢查 Docker 容器
check_container() {
    local container=$1
    local expected_status="Up"
    
    if docker ps --format "{{.Names}}" | grep -q "$container"; then
        local status=$(docker ps --filter "name=$container" --format "{{.Status}}" | head -1)
        if [[ $status == Up* ]]; then
            echo -e "${GREEN}✅ 容器 $container: 運行中${NC}"
            ((CHECKS_PASSED++))
            return 0
        else
            echo -e "${YELLOW}⚠️  容器 $container: 異常狀態 - $status${NC}"
            ((CHECKS_WARNED++))
            return 1
        fi
    else
        echo -e "${RED}❌ 容器 $container: 未運行${NC}"
        ((CHECKS_FAILED++))
        return 1
    fi
}

# 函數：檢查端口
check_port() {
    local port=$1
    local service=$2
    
    if netstat -tuln 2>/dev/null | grep -q ":$port " || ss -tuln 2>/dev/null | grep -q ":$port "; then
        echo -e "${GREEN}✅ 端口 $port ($service): 開放${NC}"
        ((CHECKS_PASSED++))
        return 0
    else
        echo -e "${RED}❌ 端口 $port ($service): 未開放${NC}"
        ((CHECKS_FAILED++))
        return 1
    fi
}

# 函數：檢查 URL
check_url() {
    local url=$1
    local service=$2
    
    if curl -s -f -o /dev/null "$url"; then
        echo -e "${GREEN}✅ 服務 $service: 可訪問${NC}"
        ((CHECKS_PASSED++))
        return 0
    else
        echo -e "${RED}❌ 服務 $service: 無法訪問${NC}"
        ((CHECKS_FAILED++))
        return 1
    fi
}

# 函數：檢查磁碟空間
check_disk() {
    local threshold=80
    local usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ -z "$usage" ]; then
        echo -e "${YELLOW}⚠️  磁碟空間: 無法檢測${NC}"
        ((CHECKS_WARNED++))
        return 1
    fi
    
    if [ "$usage" -lt "$threshold" ]; then
        echo -e "${GREEN}✅ 磁碟空間: ${usage}% (正常)${NC}"
        ((CHECKS_PASSED++))
        return 0
    elif [ "$usage" -lt 90 ]; then
        echo -e "${YELLOW}⚠️  磁碟空間: ${usage}% (建議清理)${NC}"
        ((CHECKS_WARNED++))
        return 1
    else
        echo -e "${RED}❌ 磁碟空間: ${usage}% (嚴重不足！)${NC}"
        ((CHECKS_FAILED++))
        return 1
    fi
}

# 函數：檢查記憶體
check_memory() {
    local threshold=85
    local usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    
    if [ -z "$usage" ]; then
        echo -e "${YELLOW}⚠️  記憶體: 無法檢測${NC}"
        ((CHECKS_WARNED++))
        return 1
    fi
    
    if [ "$usage" -lt "$threshold" ]; then
        echo -e "${GREEN}✅ 記憶體使用: ${usage}% (正常)${NC}"
        ((CHECKS_PASSED++))
        return 0
    elif [ "$usage" -lt 95 ]; then
        echo -e "${YELLOW}⚠️  記憶體使用: ${usage}% (偏高)${NC}"
        ((CHECKS_WARNED++))
        return 1
    else
        echo -e "${RED}❌ 記憶體使用: ${usage}% (嚴重不足！)${NC}"
        ((CHECKS_FAILED++))
        return 1
    fi
}

# 開始檢查
echo -e "${BLUE}📦 檢查 Docker 容器...${NC}"
check_container "mc-server" || true
check_container "chromadb" || true
check_container "ai-bot" || true
check_container "dashboard" || true
echo ""

echo -e "${BLUE}🔌 檢查網路端口...${NC}"
check_port "25565" "Minecraft" || true
check_port "8000" "ChromaDB" || true
check_port "8501" "Dashboard" || true
echo ""

echo -e "${BLUE}🌐 檢查 HTTP 服務...${NC}"
check_url "http://localhost:8501/_stcore/health" "Dashboard" || true
check_url "http://localhost:8000/api/v1/heartbeat" "ChromaDB" || true
echo ""

echo -e "${BLUE}💾 檢查系統資源...${NC}"
check_disk || true
check_memory || true

# 檢查 Docker 空間
docker_usage=$(docker system df | grep "Local Volumes" | awk '{print $4}' | sed 's/[^0-9.]//g' | head -1)
if [ ! -z "$docker_usage" ]; then
    echo -e "${BLUE}📊 Docker 空間使用: ${docker_usage}${NC}"
fi

echo ""

# 檢查最近的錯誤日誌
echo -e "${BLUE}📋 最近錯誤日誌 (最後 10 條):${NC}"
docker-compose logs --tail=100 2>/dev/null | grep -i error | tail -10 || echo "  (無錯誤日誌)"
echo ""

# 顯示容器資源使用
echo -e "${BLUE}📊 容器資源使用:${NC}"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "  (無法獲取)"
echo ""

# 總結
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}檢查結果總結:${NC}"
echo -e "${GREEN}✅ 通過: $CHECKS_PASSED${NC}"
echo -e "${YELLOW}⚠️  警告: $CHECKS_WARNED${NC}"
echo -e "${RED}❌ 失敗: $CHECKS_FAILED${NC}"
echo -e "${BLUE}======================================${NC}"

# 返回狀態碼
if [ $CHECKS_FAILED -gt 0 ]; then
    echo -e "${RED}❌ 健康檢查失敗！${NC}"
    exit 1
elif [ $CHECKS_WARNED -gt 0 ]; then
    echo -e "${YELLOW}⚠️  健康檢查有警告${NC}"
    exit 0
else
    echo -e "${GREEN}✅ 健康檢查通過！${NC}"
    exit 0
fi
