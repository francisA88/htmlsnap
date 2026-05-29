#include "AppCore/AppCore.h"
#include "Ultralight/Ultralight.h"
#include "JavaScriptCore/JavaScript.h"

#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

#define LOG std::cout<<"C++: "

using namespace ultralight;
// using namespace std;

// Keep handles globally for simplicity
static RefPtr<Renderer> g_renderer;
static RefPtr<View> g_view;

extern "C"{

void initPlatform(const char* base_path = "") {
    Platform::instance().set_font_loader(GetPlatformFontLoader());

    Platform::instance().set_file_system(GetPlatformFileSystem(base_path));

    Platform::instance().set_logger(GetDefaultLogger("ultralight.log"));
}
}

std::string getExtension(const std::string& path) {
    auto pos = path.find_last_of('.');
    if (pos == std::string::npos)
        return "";

    std::string ext = path.substr(pos + 1);

    std::transform(ext.begin(), ext.end(), ext.begin(),
                   [](unsigned char c) { return std::tolower(c); });

    return ext;
}

std::vector<int> get_element_rect(const char* selector) {
    if (!g_view || !selector){
        return {0,0,0,0};
    }

    auto lock = g_view->LockJSContext();
    
    std::string js =
        "(function(){"
        " const el = document.querySelector('" + std::string(selector) + "');"
        " if (!el) return null;"
        " const r = el.getBoundingClientRect();"
        " return `${r.left},${r.top},${r.width},${r.height}`;"
        "})()";
    
    LOG<<"Evaluating JS to get element rect: "<<js<<"\n";

    String result = g_view->EvaluateScript(String(js.c_str()));
    
    std::string str = result.utf8().data();
    std::stringstream ss(str);

    std::vector<int> rect;
    std::string part;

    while (std::getline(ss, part, ',')) {
        try {
            rect.push_back(std::stoi(part));
        } catch (const std::exception& e) {
            LOG<<"Error parsing rect value: "<<e.what()<<"\n";
            return {0,0,0,0};
        }
    }
    
    return rect;
}

extern "C"{
    
void releaseSurfacePixels();

// Initialize renderer and load HTML
void initializeRenderer(int width, int height) {
    ViewConfig config;
    config.is_accelerated = false; // Ensure we use CPU renderer

    initPlatform();

    if (!g_renderer){
        g_renderer = Renderer::Create();
        LOG<< "Renderer created" <<std::endl;
    }
    
    auto view = g_renderer->CreateView(width, height, config, nullptr);
    LOG<< "View created" <<std::endl;
    g_view = view;

    g_renderer->Update();
    g_renderer->Render();
    LOG<< "Initial render complete" <<std::endl;
}


// Force a redraw (useful when you change something)
void updateRenderer() {
    g_renderer->Update();
    g_renderer->Render();
    g_renderer->RefreshDisplay(0);
}

// Retrieve the pixel buffer pointer (RGBA8)
const void* getSurfacePixels(int* width, int* height, int* stride) {
    if (!g_view){
        LOG<<"no view?\n";
        return nullptr;
    }

    auto surface = g_view->surface();
    *width = surface->width();
    *height = surface->height();
    *stride = surface->row_bytes();

    // return surface->LockPixels();
    BitmapSurface* bitmap_surface = (BitmapSurface*)(surface);
    RefPtr<Bitmap> bitmap = bitmap_surface->bitmap();
    return bitmap->LockPixels();
}

bool renderCroppedToImage(const char* selector, const char* filename){
    if (!g_view)
        return false;
    
    int width, height, stride;
    auto pixels = getSurfacePixels(&width, &height, &stride);
    if (!pixels) return false;
    if (getExtension(filename) != "png") {
        LOG<<"Unsupported file format\n";
        releaseSurfacePixels();
        return false;
    }
    updateRenderer(); // Ensure we have the latest pixels
    
    std::vector<int> rect = get_element_rect(selector);
    int x = rect[0]; int y = rect[1];
    int w = rect[2]; int h = rect[3]; 
    if (x==0 && y==0 && w==0 && h==0) {
        LOG<<"Failed to get element rect\n";
        releaseSurfacePixels();
        return false;
    }
    const uint8_t* src = static_cast<const uint8_t*>(pixels);

    std::vector<uint8_t> cropped(w * h * 4);

    for (int row = 0; row < h; ++row) {
        const uint8_t* rowStart = src + (y + row) * stride + x * 4;

        memcpy(
            cropped.data() + row * w * 4,
            rowStart,
            w * 4
        );
    }
    bool ok = stbi_write_png(
        filename,
        w,
        h,
        4,
        cropped.data(),
        w * 4
    );
    if (ok)
        releaseSurfacePixels();
    return ok;
}


bool renderToPNG(const char* filename) {
    if (!g_view)
        return false;

    int width, height, stride;
    auto pixels = getSurfacePixels(&width, &height, &stride);
    if (!pixels) {
        LOG<<"Failed to get pixels\n";
        return false;
    }
    if (getExtension(filename) != "png") {
        LOG<<"Unsupported file format\n";
        releaseSurfacePixels();
        return false;
    }
    // Save as PNG using stb_image_write
    int result = stbi_write_png(filename, width, height, 4, pixels, stride);

    releaseSurfacePixels();
    
    return result != 0;
}
// Release the lock when done
void releaseSurfacePixels() {
    // RefPtr<View> view = g_views[surface_id];
    if (g_view)
        g_view->surface()->UnlockPixels();
}

bool loadURL(const char* url) {
    if (!g_view)
        return false;
    g_view->LoadURL(url);
    return true;
}

bool loadHTML(const char* html) {
    if (!g_view)
        return false;
    g_view->LoadHTML(html);
    return true;
}
// Cleanup everything
void destroySurface() {
    if (!g_view) return;
    g_view = nullptr;
}

void destroyRenderer(){
    g_renderer = nullptr;
    // free(&g_renderer);
}


} // extern "C"