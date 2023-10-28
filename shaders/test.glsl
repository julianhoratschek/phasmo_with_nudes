// uniform vec2 playerPosition;

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;

    fragColor = mix(texture(iChannel0, uv), vec4(0, 0, 0, 1), smoothstep(0.0, 0.3, distance(uv, vec2(0.5, 0.5))));
}