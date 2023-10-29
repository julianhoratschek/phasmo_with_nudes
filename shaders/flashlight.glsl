// uniform vec2 playerPosition;

uniform const vec2 Center = vec2(0.5, 0.5);
uniform const float Cone = 4.5;
uniform const float LightLength = 1.5;
uniform const float Flicker = 0.004;

float rand() {
    return fract(sin(iTime * iMouse.x) * 1024);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    vec2 mouse_uv = iMouse.xy / iResolution.xy;

    vec2 center_uv = uv - Center;
    vec2 center_mouse = mouse_uv - Center;

    float a = pow(dot(normalize(center_uv), normalize(center_mouse)), Cone);

    float intensity = a * mix(0.0, 1.0, 1.0 - length(center_uv) * LightLength);

    fragColor = texture(iChannel0, uv) * intensity * step(Flicker, rand());
}