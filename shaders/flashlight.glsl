// uniform vec2 playerPosition;

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    vec2 mouse_uv = iMouse.xy / iResolution.xy;

    vec2 center_uv = uv - vec2(0.5, 0.5);
    vec2 center_mouse = mouse_uv - vec2(0.5, 0.5);

    float a = pow(dot(normalize(center_uv), normalize(center_mouse)), 6);

    float intensity = a * mix(0.0, 1.0, 1.0 - length(center_uv) * 1.5);

    fragColor = texture(iChannel0, uv) * intensity * mix(0.2, 1.0, cos(noise1(iTime)));
}