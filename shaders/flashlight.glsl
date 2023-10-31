float rand() {
    return fract(sin(iTime) * 100);
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 uv = fragCoord / iResolution.xy;
    vec2 mouse_uv = iMouse.xy / iResolution.xy;

    vec2 center = uv - vec2(0.5, 0.5);
    vec2 ray_direction = mouse_uv - vec2(0.5, 0.5);

    float power = pow(dot(normalize(center), normalize(ray_direction)), 6.0);
    float light = mix(0.2, power, 1 - length(center) * 1.4);

    float shadow = 0.0;
    if(power > 0 && texture(iChannel0, uv).a == 0) {
        for (int i = 0; i < 50; i++) {
            vec2 pv = uv - (i * 0.008 * normalize(ray_direction));
            if(dot(normalize(ray_direction), normalize(pv - vec2(0.5, 0.5))) > 0)
                shadow += texture(iChannel0, pv).a / 50;
        }
    }

    fragColor = mix(vec4(0), texture(iChannel1, uv) * light, 1 - shadow * 2.3) * step(0.02, rand() * 10);
}