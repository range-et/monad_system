// Monad.h — umbrella header for the Monad Design System C++ library.
// Generated from colors.json — do not edit directly.
//
// Usage (Arduino + TFT_eSPI / Adafruit GFX):
//
//   #include <Monad.h>
//   using namespace monad;
//   tft.fillScreen(rgb565(theme::BACKGROUND));
//   tft.setTextColor(rgb565(theme::TEXT_PRIMARY), rgb565(theme::BACKGROUND));
//   tft.drawRect(0, 0, 100, 20, rgb565(theme::INTERACTIVE));
//
// Usage (SSD1306 OLED — pixel-on means white-on-black):
//
//   #include <Monad.h>
//   using namespace monad;
//   if (mono(theme::INTERACTIVE)) display.drawPixel(x, y, SSD1306_WHITE);
//
// Usage (Waveshare / GxEPD2 monochrome e-ink — ink on paper):
//
//   #define MONAD_LIGHT_THEME    // paper-like UI uses the light theme
//   #include <Monad.h>
//   using namespace monad;
//   // mono() returns true when the colour is closer to white. For e-ink
//   // we want the *dark* tokens drawn as ink, so invert with !mono.
//   uint16_t fg = !mono(theme::TEXT_PRIMARY) ? GxEPD_BLACK : GxEPD_WHITE;
//   display.setTextColor(fg);
//
// Switch theme: define MONAD_LIGHT_THEME before including this header.
//   #define MONAD_LIGHT_THEME
//   #include <Monad.h>

#pragma once

#include "MonadPalette.h"
#include "MonadMotion.h"
