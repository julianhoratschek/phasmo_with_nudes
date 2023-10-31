void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 uv = fragCoord / iResolution.xy;
    vec2 mouse_uv = iMouse.xy / iResolution.xy;

    vec2 center = uv - vec2(0.5, 0.5);
    vec2 ray_direction = mouse_uv - vec2(0.5, 0.5);

    float power = pow(dot(normalize(center), normalize(ray_direction)), 6);

    float shadow = 0.0;
    if(power > 0 && texture(iChannel0, uv).a == 0) {
        for (int i = 0; i < 50; i++) {
            shadow += texture(iChannel0, uv - (i * 0.008 * normalize(ray_direction))).a / 50;
        }
    }

    fragColor = mix(vec4(0), texture(iChannel1, uv) * power, 1 - shadow * 2.3);
}