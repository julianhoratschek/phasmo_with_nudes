

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord.xy / iResolution.xy;

    fragColor = texture(iChannel0, uv) + vec4(0.6, 0, 0, 0);
}