#!/bin/bash

##############################################################################
# YouTube Clipper - Claude Code Skill Installation Script
#
# Features:
# 1. Automatically create Skill directory
# 2. Copy all necessary files
# 3. Install Python dependencies
# 4. Check system dependencies (yt-dlp, FFmpeg)
#
# Usage:
#   bash install_as_skill.sh
##############################################################################

set -e  # Exit immediately on error

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo ""
    echo "========================================"
    echo "$1"
    echo "========================================"
    echo ""
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main function
main() {
    print_header "YouTube Clipper - Claude Code Skill Installation"

    # 1. Determine Skill directory
    SKILL_DIR="$HOME/.claude/skills/youtube-clipper"
    print_info "Target directory: $SKILL_DIR"

    # 2. Check if already exists
    if [ -d "$SKILL_DIR" ]; then
        print_warning "Skill directory already exists: $SKILL_DIR"
        read -p "Overwrite installation? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled"
            exit 0
        fi
        print_info "Deleting old version..."
        rm -rf "$SKILL_DIR"
    fi

    # 3. Create directory
    print_info "Creating Skill directory..."
    mkdir -p "$SKILL_DIR"
    print_success "Directory created"

    # 4. Copy files
    print_info "Copying project files..."

    # Get script directory (project root)
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # Copy all necessary files
    cp -r "$SCRIPT_DIR"/* "$SKILL_DIR/"

    # Exclude unnecessary files
    if [ -d "$SKILL_DIR/.git" ]; then
        rm -rf "$SKILL_DIR/.git"
    fi
    if [ -d "$SKILL_DIR/venv" ]; then
        rm -rf "$SKILL_DIR/venv"
    fi
    if [ -d "$SKILL_DIR/__pycache__" ]; then
        rm -rf "$SKILL_DIR/__pycache__"
    fi
    if [ -d "$SKILL_DIR/youtube-clips" ]; then
        rm -rf "$SKILL_DIR/youtube-clips"
    fi
    if [ -f "$SKILL_DIR/.env" ]; then
        rm "$SKILL_DIR/.env"
    fi

    print_success "File copy complete"

    # 5. Check Python
    print_info "Checking Python environment..."
    if ! command_exists python3; then
        print_error "Python 3 not found, please install Python 3.8+"
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version)
    print_success "Python installed: $PYTHON_VERSION"

    # 6. Check pip
    if ! command_exists pip3 && ! command_exists pip; then
        print_error "pip not found, please install pip first"
        exit 1
    fi
    print_success "pip installed"

    # 7. Install Python dependencies
    print_info "Installing Python dependencies..."
    cd "$SKILL_DIR"

    # Try to use pip3, fallback to pip
    if command_exists pip3; then
        pip3 install -q yt-dlp pysrt python-dotenv
    else
        pip install -q yt-dlp pysrt python-dotenv
    fi

    print_success "Python dependencies installed (yt-dlp, pysrt, python-dotenv)"

    # 8. Check yt-dlp
    print_info "Checking yt-dlp..."
    if command_exists yt-dlp; then
        YT_DLP_VERSION=$(yt-dlp --version)
        print_success "yt-dlp installed: $YT_DLP_VERSION"
    else
        print_warning "yt-dlp command-line tool not installed"
        print_info "Installation methods:"
        print_info "  macOS:  brew install yt-dlp"
        print_info "  Ubuntu: sudo apt-get install yt-dlp"
        print_info "  Or: pip3 install -U yt-dlp"
    fi

    # 9. Check FFmpeg (critical: needs libass support)
    print_header "Checking FFmpeg (required for subtitle burning)"

    FFMPEG_FOUND=false
    LIBASS_SUPPORTED=false

    # Check ffmpeg-full (recommended for macOS)
    if [ -f "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg" ]; then
        print_success "ffmpeg-full installed (Apple Silicon)"
        FFMPEG_FOUND=true
        LIBASS_SUPPORTED=true
    elif [ -f "/usr/local/opt/ffmpeg-full/bin/ffmpeg" ]; then
        print_success "ffmpeg-full installed (Intel Mac)"
        FFMPEG_FOUND=true
        LIBASS_SUPPORTED=true
    elif command_exists ffmpeg; then
        FFMPEG_VERSION=$(ffmpeg -version | head -n 1)
        print_success "FFmpeg installed: $FFMPEG_VERSION"
        FFMPEG_FOUND=true

        # Check libass support
        if ffmpeg -filters 2>&1 | grep -q "subtitles"; then
            print_success "FFmpeg supports libass (subtitle burning available)"
            LIBASS_SUPPORTED=true
        else
            print_warning "FFmpeg does not support libass (subtitle burning unavailable)"
        fi
    fi

    if [ "$FFMPEG_FOUND" = false ]; then
        print_error "FFmpeg not installed"
        print_info "Installation methods:"
        print_info "  macOS:  brew install ffmpeg-full  # Recommended, includes libass"
        print_info "  Ubuntu: sudo apt-get install ffmpeg libass-dev"
    elif [ "$LIBASS_SUPPORTED" = false ]; then
        print_warning "FFmpeg lacks libass support, subtitle burning will be unavailable"
        print_info "Fix (macOS):"
        print_info "  brew uninstall ffmpeg"
        print_info "  brew install ffmpeg-full"
    fi

    # 10. Create .env file
    print_header "Configuring Environment Variables"

    if [ -f "$SKILL_DIR/.env.example" ]; then
        print_info "Creating .env file..."
        cp "$SKILL_DIR/.env.example" "$SKILL_DIR/.env"
        print_success ".env file created"
        echo ""
        print_info "Config file location: $SKILL_DIR/.env"
        print_info "To customize config, edit:"
        print_info "  nano $SKILL_DIR/.env"
        print_info "  or"
        print_info "  code $SKILL_DIR/.env"
    else
        print_warning ".env.example file not found"
    fi

    # 11. Complete
    print_header "Installation Complete!"

    print_success "YouTube Clipper successfully installed as Claude Code Skill"
    echo ""
    print_info "Installation location: $SKILL_DIR"
    echo ""

    # Check dependency status
    if [ "$FFMPEG_FOUND" = false ] || [ "$LIBASS_SUPPORTED" = false ]; then
        print_warning "System dependencies incomplete, some features might be unavailable"
        echo ""
    fi

    print_info "Usage:"
    print_info "  In Claude Code run:"
    print_info "  \"Clip this YouTube video: https://youtube.com/watch?v=VIDEO_ID\""
    echo ""
    print_info "Documentation:"
    print_info "  - Skill Guide: $SKILL_DIR/SKILL.md"
    print_info "  - Project Guide: $SKILL_DIR/README.md"
    print_info "  - Technical Notes: $SKILL_DIR/TECHNICAL_NOTES.md"
    echo ""
    print_success "Enjoy! 🎉"
    echo ""
}

# Error handling
trap 'print_error "Error occurred during installation"; exit 1' ERR

# Run main function
main
